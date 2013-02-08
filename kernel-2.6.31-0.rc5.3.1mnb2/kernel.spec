# -*- Mode: rpm-spec -*-
#
# This Specfile is based on kernel-tmb spec done by
# Thomas Backlund <tmb@mandriva.org>
# 
# The mkflavour() macroization done by Anssi Hannula <anssi@mandriva.org>
#
# Manbo kernels now use kernel.org versioning
#
%define kernelversion	2
%define patchlevel	6
%define sublevel	31

# Package release
%define mnbrel		1

# kernel Makefile extraversion is substituted by 
# kpatch/kgit/kstable wich are either 0 (empty), rc (kpatch), git (kgit) 
# or stable release (kstable)
%define kpatch		rc5
%define kstable		0
# kernel.org -gitX patch (only the number after "git")
%define kgit		3

# Used when building update candidates
#define uclevel uc1
%define devel_notice %{?uclevel:NOTE: This is work-in-progress (WIP) development kernel.}

# kernel base name (also name of srpm)
%define kname 		kernel

# Patch tarball tag
%define ktag		mnb

# Handle manbo release
%if "%{?manbo_mkrel:has_manbo}" == "has_manbo"

%define rpmtag		%manbo_distsuffix
%if %kpatch
%if %kgit
%define rpmrel		%manbo_mkrel 0.%{kpatch}.%{kgit}.%{mnbrel}%{?uclevel:.%{uclevel}}
%else
%define rpmrel		%manbo_mkrel 0.%{kpatch}.%{mnbrel}%{?uclevel:.%{uclevel}}
%endif
%else
%define rpmrel		%manbo_mkrel %{mnbrel}%{?uclevel:.%{uclevel}}
%endif
%define fakerel 	%manbo_mkrel 1

%else

%define rpmtag		%distsuffix
%if %kpatch
%if %kgit
%define rpmrel		%mkrel 0.%{kpatch}.%{kgit}.%{mnbrel}%{?uclevel:.%{uclevel}}
%else
%define rpmrel		%mkrel 0.%{kpatch}.%{mnbrel}%{?uclevel:.%{uclevel}}
%endif
%else
%define rpmrel		%mkrel %{mnbrel}%{?uclevel:.%{uclevel}}
%endif
%define fakerel 	%mkrel 1

%endif

# fakerel above and fakever below never change, they are used to fool
# rpm/urpmi/smart
%define fakever		1

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %kpatch
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver	  	%{kernelversion}.%{patchlevel}.%(expr %{sublevel} - 1)
%define patch_ver 	%{kversion}-%{kpatch}-%{ktag}%{mnbrel}
%else
%if %kstable
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}.%{kstable}
%define tar_ver   	%{kernelversion}.%{patchlevel}.%{sublevel}
%else
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver   	%{kversion}
%endif
%define patch_ver 	%{kversion}-%{ktag}%{mnbrel}
%endif
%define kverrel   	%{kversion}-%{rpmrel}

# Used for not making too long names for rpms or search paths
%if %kpatch
%if %kgit
%define buildrpmrel     0.%{kpatch}.%{kgit}.%{mnbrel}%{?uclevel:.%{uclevel}}%{rpmtag}
%else
%define buildrpmrel     0.%{kpatch}.%{mnbrel}%{?uclevel:.%{uclevel}}%{rpmtag}
%endif
%else
%define buildrpmrel     %{mnbrel}%{?uclevel:.%{uclevel}}%{rpmtag}
%endif
%define buildrel     	%{kversion}-%{buildrpmrel}

# Having different top level names for packges means that you have to remove
# them by hard :(
%define top_dir_name 	%{kname}-%{_arch}

%define build_dir 	${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir 	%{build_dir}/linux-%{tar_ver}

# Disable useless debug rpms...
%define _enable_debug_packages 	%{nil}
%define debug_package 		%{nil}

# Build defines
%define build_doc 		1
%define build_source 		1
%define build_devel 		1
%define build_debug 		1

# Build desktop i586 / 1GB
%ifarch %{ix86}
%define build_desktop586	1
%endif

# Build desktop (i686 / 4GB) / x86_64 / sparc64 sets
%define build_desktop		1

# Build server (i686 / 64GB)/x86_64 / sparc64 sets
%define build_server		1

# End of user definitions
%{?_without_desktop586: %global build_desktop586 0}
%{?_without_desktop: %global build_desktop 0}
%{?_without_server: %global build_server 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}
%{?_without_debug: %global build_debug 0}

%{?_with_desktop586: %global build_desktop586 1}
%{?_with_desktop: %global build_desktop 1}
%{?_with_server: %global build_server 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}
%{?_with_debug: %global build_debug 1}

# For the .nosrc.rpm
%define build_nosrc 	0
%{?_with_nosrc: %global build_nosrc 1}

%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC"
%else
%define kmake %make
%endif
# there are places where parallel make don't work
%define smake make

# Parallelize xargs invocations on smp machines
%define kxargs xargs %([ -z "$RPM_BUILD_NCPUS" ] \\\
	&& RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"; \\\
	[ "$RPM_BUILD_NCPUS" -gt 1 ] && echo "-P $RPM_BUILD_NCPUS")

# Sparc arch wants sparc64 kernels
%define target_arch    %(echo %{_arch} | sed -e "s/sparc/sparc64/")


#
# SRC RPM description
#
Summary: 	Linux kernel built for Manbo
Name:		%{kname}
Version: 	%{kversion}
Release: 	%{rpmrel}
License: 	GPLv2
Group: 	 	System/Kernel and hardware
ExclusiveArch: %{ix86} ppc powerpc x86_64 amd64 sparc sparc64
ExclusiveOS: 	Linux
URL:            http://wiki.mandriva.com/en/Manbo_Core2_kernel

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign
### This is for stripped SRC RPM
%if %build_nosrc
NoSource: 0
%endif
# This is for disabling *config, mrproper, prepare, scripts on -devel rpms
Source2: 	disable-mrproper-in-devel-rpms.patch
Source3:	disable-prepare-scripts-configs-in-devel-rpms.patch

Source4: 	README.kernel-sources
Source5: 	README.MandrivaLinux

Source100: 	linux-%{patch_ver}.tar.bz2

####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v2.6/testing

%if %kpatch
Patch1:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2.sign
%endif
%if %kgit
Patch2:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-git%{kgit}.bz2
Source11: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-git%{kgit}.bz2.sign
%endif
%if %kstable
Patch1:   	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2.sign
%endif

#END
####################################################################

# Defines for the things that are needed for all the kernels
#
%define common_description_kernel The kernel package contains the Linux kernel (vmlinuz), the core of your \
Manbo Linux operating system. The kernel handles the basic functions \
of the operating system: memory allocation, process allocation, device \
input and output, etc.

%define common_description_info For instructions for update, see:	\
http://www.mandriva.com/en/security/kernelupdate			\
									\
%{devel_notice}

### Global Requires/Provides
%define requires1	bootloader-utils >= 1.13-1
%define requires2	mkinitrd >= 4.2.17-31
%define requires3	module-init-tools >= 3.0-7
%define requires4	sysfsutils >= 1.3.0-1
%define requires5	kernel-firmware >= 2.6.27-0.rc2.2mdv

%define kprovides 	%{kname} = %{kverrel}, kernel = %{tar_ver}, alsa = 1.0.20, drbd-api = 88

%define kconflicts	drakxtools-backend < 10.4.190-2

%define kobsoletes	dkms-iwlwifi < 1.2.26

BuildRoot: 		%{_tmppath}/%{kname}-%{kversion}-%{_arch}-build
Autoreqprov: 		no
BuildRequires: 		gcc module-init-tools

%description
%common_description_kernel

%common_description_info

# Virtual kernel rpm to help the installer during the naming transition,
# consider removing it after 2008.0 release
%package -n %{kname}-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
Summary:	Virtual rpm for installing the default %{kname}
Group:		System/Kernel and hardware
Requires:	%{kname}-desktop-%{buildrel}
%description -n %{kname}-%{buildrel}
This package is a virtual rpm that helps the installer to install
the default %{kname} during the transition to the new naming scheme.

%common_description_info

%files -n %{kname}-%{buildrel}
%defattr(-,root,root)

# Define obsolete/provides to help automatic upgrades of old kernel
# flavours to the new ones. Can probably be removed when 2007.1 gets EOL.
# And have desktop kernel replace laptop one that is no longer built
%define latest_obsoletes_desktop kernel-latest < 2.6.22-7, kernel-laptop-latest < 2.6.25
%define latest_provides_desktop kernel-latest = %{kverrel}, kernel-laptop-latest = %{kverrel}
%ifarch %{ix86}
%define latest_obsoletes_desktop586 kernel-legacy-latest < 2.6.22-7
%define latest_provides_desktop586 kernel-legacy-latest = %{kverrel}
%define latest_obsoletes_server kernel-enterprise-latest < 2.6.22-7
%define latest_provides_server kernel-enterprise-latest = %{kverrel}
%endif
# Make kernel-desktop-devel-latest obsolete kernel-source-stripped-latest
# it's not a perfect match, but it's better than full source, and it does work
# And have desktop kernel-devel replace old laptop one
%define latest_obsoletes_devel_desktop kernel-source-stripped-latest < 2.6.22-7, kernel-laptop-devel-latest < 2.6.25
%define latest_provides_devel_desktop kernel-source-stripped-latest = %{kverrel}, kernel-laptop-devel-latest = %{kverrel}

# mkflavour() name flavour processor
# name: the flavour name in the package name
# flavour: first parameter of CreateKernel()
%define mkflavour()					\
%package -n %{kname}-%{1}-%{buildrel}			\
Version:	%{fakever}				\
Release:	%{fakerel}				\
Provides:	%kprovides				\
Requires(pre):	%requires1 %requires2 %requires3 %requires4 \
Requires:	%requires5				\
Provides:	should-restart = system			\
Suggests:	crda					\
Obsoletes:	%kobsoletes				\
Conflicts:	%kconflicts				\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
Summary:	%{expand:%{summary_%(echo %{1})}}	\
Group:		System/Kernel and hardware		\
%description -n %{kname}-%{1}-%{buildrel}		\
%common_description_kernel %{expand:%{info_%(echo %{1})}} \
							\
%common_description_info				\
							\
%package -n	%{kname}-%{1}-devel-%{buildrel}		\
Version:	%{fakever}				\
Release:	%{fakerel}				\
Requires:	glibc-devel ncurses-devel make gcc perl	\
Summary:	The kernel-devel files for %{kname}-%{1}-%{buildrel} \
Group:		Development/Kernel			\
Provides:	kernel-devel = %{kverrel} 		\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
%description -n %{kname}-%{1}-devel-%{buildrel}		\
This package contains the kernel files (headers and build tools) \
that should be enough to build additional drivers for   \
use with %{kname}-%{1}-%{buildrel}.                     \
							\
If you want to build your own kernel, you need to install the full \
%{kname}-source-%{buildrel} rpm.			\
							\
%common_description_info				\
							\
%package -n	%{kname}-%{1}-debug-%{buildrel}		\
Version:	%{fakever}				\
Release:	%{fakerel}				\
Summary:	Files with debug info for %{kname}-%{1}-%{buildrel} \
Group:		Development/Debug			\
Provides:	kernel-debug = %{kverrel} 		\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
%description -n %{kname}-%{1}-debug-%{buildrel}		\
This package contains the files with debug info to aid in debug tasks \
when using %{kname}-%{1}-%{buildrel}.			\
							\
If you need to look at debug information or use some application that \
needs debugging info from the kernel, this package may help. \
							\
%common_description_info				\
							\
%package -n %{kname}-%{1}-latest			\
Version:	%{kversion}				\
Release:	%{rpmrel}				\
Summary:	Virtual rpm for latest %{kname}-%{1}	\
Group:		System/Kernel and hardware		\
Requires:	%{kname}-%{1}-%{buildrel}		\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
%{expand:%%{?latest_obsoletes_%{1}:Obsoletes: %{latest_obsoletes_%{1}}}} \
%{expand:%%{?latest_provides_%{1}:Provides: %{latest_provides_%{1}}}} \
%description -n %{kname}-%{1}-latest			\
This package is a virtual rpm that aims to make sure you always have the \
latest %{kname}-%{1} installed...			\
							\
%common_description_info				\
							\
%package -n %{kname}-%{1}-devel-latest			\
Version:	%{kversion}				\
Release:	%{rpmrel}				\
Summary:	Virtual rpm for latest %{kname}-%{1}-devel \
Group:		Development/Kernel			\
Requires:	%{kname}-%{1}-devel-%{buildrel}		\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
Provides:	%{kname}-devel-latest			\
%{expand:%%{?latest_obsoletes_devel_%{1}:Obsoletes: %{latest_obsoletes_devel_%{1}}}} \
%{expand:%%{?latest_provides_devel_%{1}:Provides: %{latest_provides_devel_%{1}}}} \
%description -n %{kname}-%{1}-devel-latest		\
This package is a virtual rpm that aims to make sure you always have the \
latest %{kname}-%{1}-devel installed...			\
							\
%common_description_info				\
							\
%package -n %{kname}-%{1}-debug-latest			\
Version:	%{kversion}				\
Release:	%{rpmrel}				\
Summary:	Virtual rpm for latest %{kname}-%{1}-debug \
Group:		Development/Debug			\
Requires:	%{kname}-%{1}-debug-%{buildrel}		\
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
Provides:	%{kname}-debug-latest			\
%description -n %{kname}-%{1}-debug-latest		\
This package is a virtual rpm that aims to make sure you always have the \
latest %{kname}-%{1}-debug installed...			\
							\
%common_description_info				\
							\
%post -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-post \
%preun -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-preun \
%postun -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-postun \
							\
%post -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-post \
%preun -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-preun \
							\
%files -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1} \
%files -n %{kname}-%{1}-latest				\
%defattr(-,root,root)					\
							\
%if %build_devel					\
%files -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1} \
%files -n %{kname}-%{1}-devel-latest			\
%defattr(-,root,root)					\
%endif							\
							\
%if %build_debug					\
%files -n %{kname}-%{1}-debug-%{buildrel} -f kernel_debug_files.%{1} \
%files -n %{kname}-%{1}-debug-latest			\
%defattr(-,root,root)					\
%endif

%ifarch %{ix86}
#
# kernel-desktop586: i586, smp-alternatives, 4GB
#

%if %build_desktop586
%define summary_desktop586 Linux kernel for desktop use with i586 & 4GB RAM
%define info_desktop586 This kernel is compiled for desktop use, single or \
multiple i586 processor(s)/core(s) and less than 4GB RAM, using voluntary \
preempt, CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%mkflavour desktop586
%endif
%endif

#
# kernel-desktop: i686, smp-alternatives, 4 GB / x86_64
#

%if %build_desktop
%ifarch %{ix86}
%define summary_desktop Linux Kernel for desktop use with i686 & 4GB RAM
%define info_desktop This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_1000, \
voluntary preempt, CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_desktop Linux Kernel for desktop use with %{_arch}
%define info_desktop This kernel is compiled for desktop use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_1000, voluntary preempt, \
CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour desktop
%endif

#
# kernel-server: i686, smp-alternatives, 64 GB / x86_64
#

%if %build_server
%ifarch %{ix86}
%define summary_server Linux Kernel for server use with i686 & 64GB RAM
%define info_server This kernel is compiled for server use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using \
no preempt, HZ_100, CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_server Linux Kernel for server use with %{_arch}
%define info_server This kernel is compiled for server use, single or \
multiple %{_arch} processor(s)/core(s), using no preempt, HZ_100, \
CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour server
%endif

#
# kernel-source
#
%package -n %{kname}-source-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The Linux source code for %{kname}-%{buildrel}  
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source = %{kverrel}, kernel-devel = %{kverrel}
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-source-%{buildrel}
The %{kname}-source package contains the source code files for the Manbo
Linux kernel. Theese source files are only needed if you want to build your
own custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

%common_description_info

%post -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{kversion}-{desktop586,desktop,server}-%{buildrpmrel}; do
        if [ -d $i ]; then
		if [ ! -L $i/build -a ! -L $i/source ]; then
			ln -sf /usr/src/linux-%{kversion}-%{buildrpmrel} $i/build
			ln -sf /usr/src/linux-%{kversion}-%{buildrpmrel} $i/source
		fi
        fi
done
cd /usr/src
rm -f linux
ln -snf linux-%{kversion}-%{buildrpmrel} linux

%preun -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{kversion}-{desktop586,desktop,server}-%{buildrpmrel}/{build,source}; do
	if [ -L $i ]; then
		if [ "$(readlink $i)" = "/usr/src/linux-%{kversion}-%{buildrpmrel}" ]; then
			rm -f $i
		fi
	fi
done
if [ -L /usr/src/linux ]; then
	if [ "$(readlink /usr/src/linux)" = "linux-%{kversion}-%{buildrpmrel}" ]; then
		rm -f /usr/src/linux
	fi
fi
exit 0

#
# kernel-source-latest: virtual rpm
#
%package -n %{kname}-source-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group:   	Development/Kernel
Requires: 	%{kname}-source-%{buildrel}
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...

%common_description_info

#
# kernel-doc: documentation for the Linux kernel
#
%package -n %{kname}-doc
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Various documentation bits found in the %{kname} source
Group: 		Books/Computer books
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-doc
This package contains documentation files from the %{kname} source. 
Various bits of information about the Linux kernel and the device drivers 
shipped with it are documented in these files. You also might want install 
this package if you need a reference to the options that can be passed to 
Linux kernel modules at load time.

%common_description_info

#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c
%setup -q -n %top_dir_name -D -T -a100

%define patches_dir ../%{patch_ver}/

cd %src_dir
%if %kpatch
%patch1 -p1
%endif
%if %kgit
%patch2 -p1
%endif
%if %kstable
%patch1 -p1
%endif

%{patches_dir}/scripts/apply_patches

# PATCH END


#
# Setup Begin
#

# Prepare all the variables for calling create_configs

%if %build_debug
%define debug --debug
%else
%define debug --no-debug
%endif

%{patches_dir}/scripts/create_configs %debug --user_cpu="%{target_arch}"

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile

# get rid of unwanted files
find . -name '*~' -o -name '*.orig' -o -name '*.append' | %kxargs rm -f


%build
# Common target directories
%define _kerneldir /usr/src/linux-%{kversion}-%{buildrpmrel}
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _efidir %{_bootdir}/efi/mandriva

# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}

PrepareKernel() {
	name=$1
	extension=$2
	x86_dir=arch/x86/configs

	echo "Make config for kernel $extension"

	%smake -s mrproper

	if [ "%{target_arch}" == "i386" -o "%{target_arch}" == "x86_64" ]; then
	    if [ -z "$name" ]; then
		cp ${x86_dir}/%{target_arch}_defconfig-desktop .config
	    else
		cp ${x86_dir}/%{target_arch}_defconfig-$name .config
	    fi
	else
	    if [ -z "$name" ]; then
		cp arch/%{target_arch}/defconfig-desktop .config
	    else
		cp arch/%{target_arch}/defconfig-$name .config
	    fi
	fi

	# make sure EXTRAVERSION says what we want it to say
	%if %kstable
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{kstable}-$extension/" Makefile
	%else
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
	%endif

	%smake oldconfig
}

BuildKernel() {
	KernelVer=$1

	echo "Building kernel $KernelVer"

	%kmake all

	# Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer
	gzip -c Module.symvers > %{temp_boot}/symvers-$KernelVer.gz

        %ifarch ppc powerpc
	        cp -f vmlinux %{temp_boot}/vmlinuz-$KernelVer
		%ifarch ppc
			cp -f arch/ppc/boot/images/zImage.chrp-rs6k %{temp_boot}/vmlinuz-rs6k-$KernelVer
		%endif
	%else
	%ifarch sparc sparc64
		gzip -9c vmlinux > %{temp_boot}/vmlinuz-$KernelVer
	%else
		cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 

	# remove /lib/firmware, we use a separate kernel-firmware
	rm -rf %{temp_root}/lib/firmware
}

SaveDevel() {
	devel_flavour=$1

	DevelRoot=/usr/src/linux-%{kversion}-$devel_flavour-%{buildrpmrel}
	TempDevelRoot=%{temp_root}$DevelRoot

	mkdir -p $TempDevelRoot
	for i in $(find . -name 'Makefile*'); do cp -R --parents $i $TempDevelRoot;done
	for i in $(find . -name 'Kconfig*' -o -name 'Kbuild*'); do cp -R --parents $i $TempDevelRoot;done
	cp -fR include $TempDevelRoot
	cp -fR scripts $TempDevelRoot
	cp -fR kernel/bounds.c $TempDevelRoot/kernel
	%ifarch %{ix86} x86_64
		cp -fR arch/x86/kernel/asm-offsets.{c,s} $TempDevelRoot/arch/x86/kernel/
		cp -fR arch/x86/kernel/asm-offsets_{32,64}.c $TempDevelRoot/arch/x86/kernel/
		cp -fR arch/x86/include $TempDevelRoot/arch/x86/
	%else
		cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} $TempDevelRoot/arch/%{target_arch}/kernel/
		cp -fR arch/%{target_arch}/include $TempDevelRoot/arch/%{target_arch}/
	%endif
	cp -fR .config Module.symvers $TempDevelRoot
	cp -fR 3rdparty/mkbuild.pl $TempDevelRoot/3rdparty

	# Needed for truecrypt build (Danny)
	cp -fR drivers/md/dm.h $TempDevelRoot/drivers/md/

	# Needed for lguest
	cp -fR drivers/lguest/lg.h $TempDevelRoot/drivers/lguest/

	# Needed for lirc_gpio (#39004)
	cp -fR drivers/media/video/bt8xx/bttv{,p}.h $TempDevelRoot/drivers/media/video/bt8xx/

	# Needed for external dvb tree (#41418)
	cp -fR drivers/media/dvb/dvb-core/*.h $TempDevelRoot/drivers/media/dvb/dvb-core/
	cp -fR drivers/media/dvb/frontends/lgdt330x.h $TempDevelRoot/drivers/media/dvb/frontends/
	# http://lists.mandriva.com/cooker/2009-05/msg00534.php
	cp -fR drivers/ieee1394/*.h $TempDevelRoot/drivers/ieee1394/

	# add acpica header files, needed for fglrx build
	cp -fR drivers/acpi/acpica/*.h $TempDevelRoot/drivers/acpi/acpica/

	for i in alpha arm avr32 blackfin cris frv h8300 ia64 m32r m68knommu \
	         microblaze mips mn10300 parisc s390 sh xtensa; do
		rm -rf $TempDevelRoot/arch/$i
		rm -rf $TempDevelRoot/include/asm-$i
	done

	# ppc needs only m68k headers
	rm -rf $TempDevelRoot/arch/m68k

	%ifnarch ppc powerpc
		rm -rf $TempDevelRoot/arch/powerpc
		rm -rf $TempDevelRoot/include/asm-m68k
	%endif
	%ifnarch sparc sparc64
		rm -rf $TempDevelRoot/arch/sparc
		rm -rf $TempDevelRoot/arch/sparc64
	%endif
	%ifnarch %{ix86} x86_64
		rm -rf $TempDevelRoot/arch/x86
		rm -rf $TempDevelRoot/include/asm-x86
	%endif

	# Clean the scripts tree, and make sure everything is ok (sanity check)
	# running prepare+scripts (tree was already "prepared" in build)
	pushd $TempDevelRoot >/dev/null
		%smake -s prepare scripts
		%smake -s clean
	popd >/dev/null
	rm -f $TempDevelRoot/.config.old

	# fix permissions
	chmod -R a+rX $TempDevelRoot

	# disable mrproper in -devel rpms
	patch -p1 --fuzz=0 -d $TempDevelRoot -i %{SOURCE2}
	patch -p1 --fuzz=0 -d $TempDevelRoot -i %{SOURCE3}

	kernel_devel_files=../kernel_devel_files.$devel_flavour


### Create the kernel_devel_files.*
cat > $kernel_devel_files <<EOF
%defattr(-,root,root)
%dir $DevelRoot
%dir $DevelRoot/arch
%dir $DevelRoot/include
$DevelRoot/3rdparty
$DevelRoot/Documentation
%ifarch ppc powerpc
$DevelRoot/arch/powerpc
$DevelRoot/arch/ppc
%endif
%ifarch sparc sparc64
$DevelRoot/arch/sparc
$DevelRoot/arch/sparc64
%endif
$DevelRoot/arch/um
%ifarch %{ix86} x86_64
$DevelRoot/arch/x86
%endif
$DevelRoot/block
$DevelRoot/crypto
$DevelRoot/drivers
$DevelRoot/firmware
$DevelRoot/fs
$DevelRoot/include/Kbuild
$DevelRoot/include/acpi
$DevelRoot/include/asm
$DevelRoot/include/asm-generic
%ifarch powerpc ppc
$DevelRoot/include/asm-m68k
$DevelRoot/include/asm-powerpc
$DevelRoot/include/asm-ppc
%endif
%ifarch sparc sparc64
$DevelRoot/include/asm-sparc
$DevelRoot/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
$DevelRoot/include/asm-x86
%endif
$DevelRoot/include/config
$DevelRoot/include/crypto
$DevelRoot/include/drm
$DevelRoot/include/keys
$DevelRoot/include/linux
$DevelRoot/include/math-emu
$DevelRoot/include/media
$DevelRoot/include/mtd
$DevelRoot/include/net
$DevelRoot/include/pcmcia
$DevelRoot/include/rdma
$DevelRoot/include/rxrpc
$DevelRoot/include/scsi
$DevelRoot/include/sound
$DevelRoot/include/trace
$DevelRoot/include/video
$DevelRoot/include/xen
$DevelRoot/init
$DevelRoot/ipc
$DevelRoot/kernel
$DevelRoot/lib
$DevelRoot/mm
$DevelRoot/net
$DevelRoot/samples
$DevelRoot/scripts
$DevelRoot/security
$DevelRoot/sound
$DevelRoot/tools
$DevelRoot/usr
$DevelRoot/.config
$DevelRoot/Kbuild
$DevelRoot/Makefile
$DevelRoot/Module.symvers
$DevelRoot/arch/Kconfig
%doc README.MandrivaLinux
%doc README.kernel-sources
EOF


### Create -devel Post script on the fly
cat > $kernel_devel_files-post <<EOF
if [ -d /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel} ]; then
	rm -f /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/{build,source}
	ln -sf $DevelRoot /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/build
	ln -sf $DevelRoot /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/source
fi
EOF


### Create -devel Preun script on the fly
cat > $kernel_devel_files-preun <<EOF
if [ -L /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/build ]; then
	rm -f /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/build
fi
if [ -L /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/source ]; then
	rm -f /lib/modules/%{kversion}-$devel_flavour-%{buildrpmrel}/source
fi
exit 0
EOF
}

SaveDebug() {
	debug_flavour=$1

	install -m 644 vmlinux \
	      %{temp_boot}/vmlinux-%{kversion}-$debug_flavour-%{buildrpmrel}
	kernel_debug_files=../kernel_debug_files.$debug_flavour
	echo "%defattr(-,root,root)" > $kernel_debug_files
	echo "%{_bootdir}/vmlinux-%{kversion}-$debug_flavour-%{buildrpmrel}" \
		>> $kernel_debug_files

	find %{temp_modules}/%{kversion}-$debug_flavour-%{buildrpmrel}/kernel \
		-name "*.ko" | \
		%kxargs -I '{}' objcopy --only-keep-debug '{}' '{}'.debug
	find %{temp_modules}/%{kversion}-$debug_flavour-%{buildrpmrel}/kernel \
		-name "*.ko" | %kxargs -I '{}' \
		sh -c 'cd `dirname {}`; \
		       objcopy --add-gnu-debuglink=`basename {}`.debug \
		       --strip-debug `basename {}`'

	pushd %{temp_modules}
	find %{kversion}-$debug_flavour-%{buildrpmrel}/kernel \
		-name "*.ko.debug" > debug_module_list
	popd
	cat %{temp_modules}/debug_module_list | \
		sed 's|\(.*\)|%{_modulesdir}/\1|' >> $kernel_debug_files
	cat %{temp_modules}/debug_module_list | \
		sed 's|\(.*\)|%exclude %{_modulesdir}/\1|' \
		>> ../kernel_exclude_debug_files.$debug_flavour
	rm -f %{temp_modules}/debug_module_list
}

CreateFiles() {
	kernel_flavour=$1

	kernel_files=../kernel_files.$kernel_flavour

### Create the kernel_files.*
cat > $kernel_files <<EOF
%defattr(-,root,root)
%{_bootdir}/System.map-%{kversion}-$kernel_flavour-%{buildrpmrel}
%{_bootdir}/symvers-%{kversion}-$kernel_flavour-%{buildrpmrel}.gz
%{_bootdir}/config-%{kversion}-$kernel_flavour-%{buildrpmrel}
%{_bootdir}/vmlinuz-%{kversion}-$kernel_flavour-%{buildrpmrel}
%dir %{_modulesdir}/%{kversion}-$kernel_flavour-%{buildrpmrel}/
%{_modulesdir}/%{kversion}-$kernel_flavour-%{buildrpmrel}/kernel
%{_modulesdir}/%{kversion}-$kernel_flavour-%{buildrpmrel}/modules.*
%doc README.MandrivaLinux
%doc README.kernel-sources
EOF

	%if %build_debug
	cat ../kernel_exclude_debug_files.$kernel_flavour >> $kernel_files
	%endif

### Create kernel Post script
cat > $kernel_files-post <<EOF
/sbin/installkernel %{kversion}-$kernel_flavour-%{buildrpmrel}
pushd /boot > /dev/null
if [ -L vmlinuz-$kernel_flavour ]; then
	rm -f vmlinuz-$kernel_flavour
fi
ln -sf vmlinuz-%{kversion}-$kernel_flavour-%{buildrpmrel} vmlinuz-$kernel_flavour
if [ -L initrd-$kernel_flavour.img ]; then
	rm -f initrd-$kernel_flavour.img
fi
ln -sf initrd-%{kversion}-$kernel_flavour-%{buildrpmrel}.img initrd-$kernel_flavour.img
popd > /dev/null
%if %build_devel
# create kernel-devel symlinks if matching -devel- rpm is installed
if [ -d /usr/src/linux-%{kversion}-$kernel_flavour-%{buildrpmrel} ]; then
	rm -f /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/{build,source}
	ln -sf /usr/src/linux-%{kversion}-$kernel_flavour-%{buildrpmrel} /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/build
	ln -sf /usr/src/linux-%{kversion}-$kernel_flavour-%{buildrpmrel} /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
%if %build_source
# create kernel-source symlinks only if matching -devel- rpm is not installed
if [ -d /usr/src/linux-%{kversion}-%{buildrpmrel} -a ! -d /usr/src/linux-%{kversion}-$kernel_flavour-%{buildrpmrel} ]; then
	rm -f /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/{build,source}
	ln -sf /usr/src/linux-%{kversion}-%{buildrpmrel} /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/build
	ln -sf /usr/src/linux-%{kversion}-%{buildrpmrel} /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
EOF


### Create kernel Preun script on the fly
cat > $kernel_files-preun <<EOF
/sbin/installkernel -R %{kversion}-$kernel_flavour-%{buildrpmrel}
pushd /boot > /dev/null
if [ -L vmlinuz-$kernel_flavour ]; then
	if [ "$(readlink vmlinuz-$kernel_flavour)" = "vmlinuz-%{kversion}-$kernel_flavour-%{buildrpmrel}" ]; then
		rm -f vmlinuz-$kernel_flavour
	fi
fi
if [ -L initrd-$kernel_flavour.img ]; then
	if [ "$(readlink initrd-$kernel_flavour.img)" = "initrd-%{kversion}-$kernel_flavour-%{buildrpmrel}.img" ]; then
		rm -f initrd-$kernel_flavour.img
	fi
fi
popd > /dev/null
%if %build_devel
if [ -L /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/build ]; then
	rm -f /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/build
fi
if [ -L /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/source ]; then
	rm -f /lib/modules/%{kversion}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
exit 0
EOF


### Create kernel Postun script on the fly
cat > $kernel_files-postun <<EOF
/sbin/kernel_remove_initrd %{kversion}-$kernel_flavour-%{buildrpmrel}
EOF
}


CreateKernel() {
	flavour=$1

	PrepareKernel $flavour $flavour-%{buildrpmrel}

	BuildKernel %{kversion}-$flavour-%{buildrpmrel}
	%if %build_devel
		SaveDevel $flavour
	%endif
	%if %build_debug
		SaveDebug $flavour
	%endif
	CreateFiles $flavour
}


###
# DO it...
###


# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}


#make sure we are in the directory
cd %src_dir

%ifarch %{ix86}
%if %build_desktop586
CreateKernel desktop586
%endif
%endif

%if %build_desktop
CreateKernel desktop
%endif

%if %build_server
CreateKernel server
%endif


# We don't make to repeat the depend code at the install phase
%if %build_source
    PrepareKernel "" %{buildrpmrel}custom
%smake -s mrproper
%endif


###
### install
###
%install
install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .

cd %src_dir

# Directories definition needed for installing
%define target_source %{buildroot}%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %build_source
install -d %{target_source} 

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}

# we remove all the source files that we don't ship
# first architecture files
for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 m32r m68knommu \
         microblaze mips parisc s390 sh sh64 v850 xtensa mn10300; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i
done

# ppc needs only m68k headers
rm -rf %{target_source}/arch/m68k

%ifnarch ppc powerpc
	rm -rf %{target_source}/arch/ppc
	rm -rf %{target_source}/arch/powerpc
	rm -rf %{target_source}/include/asm-m68k
	rm -rf %{target_source}/include/asm-ppc
	rm -rf %{target_source}/include/asm-powerpc
%endif
%ifnarch sparc sparc64
	rm -rf %{target_source}/arch/sparc
	rm -rf %{target_source}/arch/sparc64
	rm -rf %{target_source}/include/asm-sparc
	rm -rf %{target_source}/include/asm-sparc64
%endif
%ifnarch %{ix86} x86_64
	rm -rf %{target_source}/arch/x86
	rm -rf %{target_source}/include/asm-x86
%endif

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.gitignore,.lst,.mailmap}
rm -f %{target_source}/{.missing-syscalls.d,arch/.gitignore,firmware/.gitignore}

#endif %build_source
%endif

# gzipping modules
find %{target_modules} -name "*.ko" | %kxargs gzip -9

# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be
for i in %{target_modules}/*; do
	rm -f $i/build $i/source
done

# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here
pushd %{target_modules}
for i in *; do
	/sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating module.description for $i"
	modules=`find . -name "*.ko.gz"`
	echo $modules | %kxargs /sbin/modinfo \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd


###
### clean
###
%clean
rm -rf %{buildroot}


# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 

###
### source and doc file lists
###

%if %build_source
%files -n %{kname}-source-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/3rdparty
%{_kerneldir}/Documentation
%{_kerneldir}/arch/Kconfig
%ifarch powerpc ppc
%{_kerneldir}/arch/powerpc
%{_kerneldir}/arch/ppc
%endif
%ifarch sparc sparc64
%{_kerneldir}/arch/sparc
%{_kerneldir}/arch/sparc64
%endif
%{_kerneldir}/arch/um
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/x86
%endif
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/firmware
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%ifarch powerpc ppc
%{_kerneldir}/include/m68k
%{_kerneldir}/include/powerpc
%{_kerneldir}/include/ppc
%endif
%ifarch sparc sparc64
%{_kerneldir}/include/asm-sparc
%{_kerneldir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_kerneldir}/include/asm-x86
%endif
%{_kerneldir}/include/crypto
%{_kerneldir}/include/drm
%{_kerneldir}/include/keys
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/media
%{_kerneldir}/include/mtd
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/rdma
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/trace
%{_kerneldir}/include/video
%{_kerneldir}/include/xen
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/virt
%{_kerneldir}/samples
%{_kerneldir}/scripts
%{_kerneldir}/security
%{_kerneldir}/sound
%{_kerneldir}/tools
%{_kerneldir}/usr
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Kbuild
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
%doc README.MandrivaLinux
%doc README.kernel-sources
#endif build_source

%files -n %{kname}-source-latest
%defattr(-,root,root)

%endif

%if %build_doc
%files -n %{kname}-doc
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif

%changelog
* Sat Aug 15 2009 Kevin Deldycke <kevin@deldycke.com> 2.6.31-0.rc5.3.1mnb-1mdv2009.1
- Backported from cooker to Mandriva 2009.1

* Fri Aug 07 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.31-0.rc5.3.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Add Sentelic touchpad support, from Dmitry Torokhov's input tree.

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.31-rc5-git3
    - update nouveau to 2009-08-07 snapshot
    - drm: add radeon rs880 pci ids, radeon kms TTM patch,
      radeon kms suspend/resume fix
    - net: core dev lockdep fix

* Sun Aug 02 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.31-0.rc5.2mnb
  o Thomas Backlund <tmb@mandriva.org>
    - update nouveau to 20090801 git snapshot
    - drop nouveau buildfix
    - fix crash in dvb-usb-af9015

* Sat Aug 01 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.31-0.rc5.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - unionfs: use atomic_long_read when reading struct file f_count
      field (f_count is atomic_long_t).

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.31-rc5
      - drop merged patches:
        usb-serial-option-add-ZTE-device-ids-and-remove-ONDA-ids.patch
        net-rfkill-fix-rfkill_set_states-to-set-the-hw-state.patch
        platform-x86-acer-wmi-rfkill-reversion.patch
      - add patches:
        - fix nouveau build with 2.6.31-rc5
      - update defconfigs

* Tue Jul 28 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.31-0.rc4.1mnb
  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.31-rc4
      - drop merged patches:
        gpu-drm-i915-hook-connector-to-encoder-during-load-detect.patch
        hwmon-coretemp-atom.patch
        input-appletouch.patch
        input-wacom-intuos4.patch
        media-video-uvc-workaround-invalid-formats.patch
        mmc-add-VIA-MSP-card-reader-driver-support.patch
        serial-8250_pci-add-OXCB950-id.patch
        sound-alsa-hda-add-acer-alc889-model.patch
        sound-alsa-hda-add-quirk-for-STAC92xx-SigmaTel-STAC9205.patch
        usb-dlink-dwm652.patch
        usb-option.c-add-a-link-3gu-device-id.patch
      - rediff patches:
        acpi-dsdt-initrd-v0.9c-fixes.patch
        fs-dynamic-nls-default.patch
        fs-sreadahead-1.0-trace-open.patch
        gpu-drm-i915-add-gem-enable-parameter.patch
        gpu-drm-mach64.patch
        input-atkbd-philco-i4xsi-release-keys.patch
        net-sis190-fix-list-usage.patch
        scsi-ppscsi-2.6.2.patch
        serial-docomo-F2402.patch
        sound-hda-codec-add-Toshiba-Pro-A200-A210-to-quirk-table.patch
        usb-serial-option-add-ZTE-device-ids-and-remove-ONDA-ids.patch
        video-mdk-logo.patch
      - add patches:
        fix ndiswrapper build with 2.6.31
        fix mach64 build with 2.6.31
        make hid-ntrig not detect HID_DG_INRANGE as TOUCH (O. Thauvin)
        fix rfkill_set_states to set the hw state
        fix reversed rfkill on acer-wmi
        add nouveau support
        re-export find_task_by_vpid symbol again, needed for Ati fglrx
        fix dell-laptop rfkill state change logic
      - update defconfigs
      - enable Character device in Userpace support (CUSE)

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Disabled on 2.6.31 default configs: CONFIG_CAN_SJA1000_PLATFORM,
      CONFIG_KEYBOARD_MATRIX, CONFIG_KEYBOARD_LM8323,
      CONFIG_BATTERY_MAX17040, CONFIG_LEDS_LP3944
      They shouldn't be needed by default pc/x86 hardware.
    - Enabled (=m): CONFIG_USB_SERIAL_QUATECH2, CONFIG_RDC_17F3101X,
      CONFIG_FB_UDL.
    - Enabled (=y): CONFIG_PCIE_ECRC.
    - rt2800usb: disable temporarily usb ids that clash with rt2870sta
      module in staging.

* Mon Jul 20 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.30.2-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - usb: Added A-Link 3GU device id 1e0e:9200 into option driver, from
      Anssi Hannula.
      Reference: http://lists.mandriva.com/kernel-discuss/2009-07/msg00003.php
    - USB: option: add ZTE device ids and remove ONDA ids.

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.30.2 (CVE-2009-1895, CVE-2009-1897)

* Sat Jul 04 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.30.1-1mnb
  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.30.1
      - drop merged patches:
        sound-intel8x0-fix-sound-skipping-introduced-in-2.6.30-rc8.patch
    - update drbd to 8.3.2
      - redo patches:
        3rd-drbd-makefile-fix.patch
        3rd-drbd-build-fixes.patch
      - add patch:
        3rd-drbd-usermode_helper.patch
    - update ndiswrapper to 1.55
      - rediff patch:
        3rd-ndiswrapper-Makefile-build-fix.patch
      - drop merged patches:
        3rd-ndiswrapper-dma_addr_t-print-warn-fix.patch
        3rd-ndiswrapper-irqreturn-warn-fix.patch
        3rd-ndiswrapper-missing-ndo-fix.patch

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Added atkbd quirk to report release events for mute, volume up and
      volume down keys on Philco I4xSI.
    - ALSA, hda: Apply upstream patch with STAC9205 new id 0x83847698
      (#41385). Fixed quirk section mismatch.
    - Enable drbd only in server kernels.
    - Remove comment from drbd Kconfig.
    - Restore 3rd-ndiswrapper-dma_addr_t-print-warn-fix.patch, not
      merged, and fix its changelog.

* Thu Jun 18 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.30-2mnb
  o Thomas Backlund <tmb@mandriva.org>
    - fix intel8x0 sound skipping introduced in 2.6.30-rc8
      (http://marc.info/?l=linux-kernel&m=124465853625485&w=2)

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Disabled CONFIG_COMEDI_PCI_DRIVERS. At least one module built with
      it enabled (s626) claims the pci id 1131:7146 for all subvendors
      and subdevice ids. The problem is that this will clash with many
      media/dvb cards that have the same main pci vendor and device ids,
      but properly specify/check subvendor and subdevice ids. For now
      just disable comedi pci drivers, in this specific case s626
      probably would need a specific subvendor/subdevice restriction in
      its pci id table or additional checks to avoid freezing when it is
      loaded on media/dvb cards with same vendor:device pci id. (#51314)
    - Include WMI stack corruption fix from Arch Linux
      Reference: http://bbs.archlinux.org/viewtopic.php?id=73877
    - Include tv/vga load-detect fix for drm/i915 from mainline
      Reference: http://lists.mandriva.com/cooker/2009-06/msg00323.php

* Fri Jun 12 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.30-1mnb
  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.30 final

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Move gpu-drm-i915-disable-gem-on-i8xx.patch to patches-broken:
      reevaluate the situation after the last drm/i915 fixes that went
      in 2.6.30
    - Unset CONFIG_UEVENT_HELPER_PATH, installer was adapted to not need
      this set in kernel config.
    - Update media-video-uvc-workaround-invalid-formats.patch with
      upstream final solution from Laurent Pinchart, "uvcvideo: Ignore
      non-UVC trailing interface descriptors".

* Wed Jun 03 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.30-0.rc8.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Switch to CONFIG_SND_DEBUG=y and CONFIG_SND_PCM_XRUN_DEBUG=y in
      kernel configs.
    - uvcvideo: workaround invalid formats exposed by buggy uvc webcams.
    - Updated to 2.6.30-rc8
      * dropped security-tomoyo-call-cap_bprm_set_creds.patch (merged)

* Mon May 25 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.30-0.rc7.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Include drivers/ieee1394 headers in kernel-*-devel packages, used
      by dkms-v4l-dvb-testing. Reference:
      http://lists.mandriva.com/cooker/2009-05/msg00534.php
    - Updated to 2.6.30-rc6
      * Redid/rediff following patches:
        hid-usbhid-quirk-multilaser.patch
        net-netfilter-psd.patch
        fs-sreadahead-1.0-trace-open.patch
        input-wacom-intuos4.patch
        acpi-dsdt-initrd-v0.9c-2.6.28.patch
        sound-alsa-hda-add-acer-alc889-model.patch
        acpi-dsdt-initrd-v0.9c-fixes.patch
        x86-p4_clockmod-reasonable-default-for-scaling_min_freq.patch
        usb-dlink-dwm652.patch
        fs-unionfs-1.4.patch
        fs-dynamic-nls-default.patch
        gpu-drm-i915-add-gem-enable-parameter.patch
        net-netfilter-IFWLOG.patch
        acpi-add-proc-event-regs.patch
        serial-docomo-F2402.patch
        3rd-drbd-build-fixes.patch
        disable-mrproper-in-devel-rpms.patch
        disable-prepare-scripts-configs-in-devel-rpms.patch
      * Removed merged fixes/additions (same patch or another solution):
        mmc-Increase-power_up-delay-to-fix-TI-readers.patch
        fs-ext4-add-EXT4_IOC_ALLOC_DA_BLKS-ioctl.patch
        fs-ext4-Automatically-allocate-delay-allocated-blocks-on-close.patch
        fs-ext4-Automatically-allocate-delay-allocated-blocks-on-rename.patch
        gpu-drm-radeon-r6xx-r7xx.patch
        gpu-drm-i915-no-gem-if-no-tiling.patch
        input-elantech-provide-workaround-for-jumpy-cursor.patch
        media-dvb-add-Yuan-PD378S.patch
        rtc-cmos.c-fixed-alias.patch
        net-mac80211-deauth-before-flushing-STA-information.patch
        net-wireless-fix-rt2x00-double-free.patch
        sound-alsa-hda-consider-additional-capsrc-alc889.patch
        sound-alsa-hda-alc882_auto_init_input_src-selector.patch
        sound-alsa-add-subdevice_mask-field-to-quirk-entries.patch
        sound-alsa-hda-92hd71xxx-disable-unmute-support-for-code.patch
        sound-alsa-hda-Additional-pin-nids-for-STAC92HD71Bx-and.patch
        sound-alsa-hda-Dynamic-detection-of-dmics-dmuxes-smuxes.patch
        sound-alsa-hda-Don-t-call-stac92xx_parse_auto_config-wi.patch
        sound-alsa-hda-Don-t-touch-non-existent-port-f-on-4-por.patch
        sound-alsa-hda-fix-speaker-output-on-hp-dv4-1155-se.patch
        sound-alsa-hda-cleanup-idt92hd7x-hp-quirks.patch
        sound-alsa-hda-cleanup-ecs202-quirks.patch
        sound-alsa-hda-Add-4-channel-mode-for-3stack-hp-model.patch
        sound-alsa-hda-Add-headphone-automute-support-for-3stac.patch
        sound-alsa-hda-Map-3stack-hp-model-ALC888-for-HP-Educ.patch
        sound-alsa-hda-Cleanup-printk-from-alc888_6st_dell_unso.patch
        video-n411-add-missing-Makefile-entry.patch
        staging-agnx-mac80211-hw-config-change-flags.patch
        staging-rtl8187se-iw_handler-fixes.patch
        security-tomoyo-1.6.7-20090401.patch
        security-tomoyo-build.patch
      * Moved sound-hda-codec-add-Sony-Vaio-VGN-FZ18M-to-quirk-table.patch
        to patches-broken, the used Vaio quirk was removed.
      * Moved uss725 patches to patches-broken: even fixing some issues
        previously, uss725 isn't working properly from reports received,
        not sure if worked well some point back in time. Stop carrying
        the patches and deprecate them.
      * Moved x86-UBUNTU-SAUCE-fix-kernel-oops-in-VirtualBox-during.patch
        to patches-broken, doesn't apply, possibly not wanted anymore.
      * Added patches with build fixes:
        fs-unionfs-use-current_umask-helper.patch
        3rd-acerhk-proc_dir_entry-owner.patch
    - Don't allow -devel mrproper patches to be applied if fuzz factor
      is greater than zero in some hunk.
    - Updated ndiswrapper to version 1.54
      * Added following warning/build fixes on top:
        3rd-ndiswrapper-dma_addr_t-print-warn-fix.patch
        3rd-ndiswrapper-missing-ndo-fix.patch
        3rd-ndiswrapper-irqreturn-warn-fix.patch
      * Dropped merged 3rd-ndiswrapper-wext_compat_2.6.27.patch
    - Add missing call to cap_bprm_set_creds in tomoyo.
    - Renamed security-tomoyo-change-boot-message-to-be-more-user-friendly.patch
      to security-tomoyo-friendly-ccs_loader-msg.patch; rebased to 2.6.30,
      changed boot message and use printk_once instead of printk

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.30-rc7
      * rediffed the following:
        acpi-add-proc-event-regs.patch
        sound-hda-codec-add-Toshiba-Pro-A200-A210-to-quirk-table.patch
      * drop the following merged patches:
        sound-oss-mixer-name.patch
    - update defconfigs

* Wed May 13 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29.3-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Update to 2.6.29.3
      * rediff usb-storage-unusual_devs-add-id.patch

* Wed May 06 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29.2-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Update to 2.6.29.2
      * removed merged patches:
        x86-platform-acer-wmi-Blacklist-Acer-Aspire-One.patch
        mm-define-a-UNIQUE-value-for-AS_UNEVICTABLE-flag.patch

* Mon Apr 20 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29.1-4mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Fixed rpm group of debug packages.
    - Back out addition of alsa patches intended for pulseaudio
      enhancements since it's causing regressions (#50120).

  o Pascal Terjan <pterjan@mandriva.com>
    - Drop sound-alsa-pcm-midlevel-Add-more-strict-buffer-position-checks-based-on-jiffies.patch
      it breaks sound in VirtualBox

* Thu Apr 16 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29.1-3mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - i915: disable gem automatically also for i8xx hardware, patch from
      Fedora. Reference: http://lists.mandriva.com/cooker/2009-04/msg00577.php
    - Added back gem_enable parameter to i915 module in case someone
      still needs it to workaround issues with gem.
    - Added patch scheduled for stable 2.6.29.x: "mm: define a UNIQUE
      value for AS_UNEVICTABLE flag".
    - Blacklist acer-wmi on Acer Aspire One, upstream patch scheduled
      for -stable.
    - More upstream ALSA patches which should help in pulseaudio issues.
    - Minor WARN redefine fix in heci 3rdparty driver.

  o Pascal Terjan <pterjan@mandriva.com>
    - Add upstream ALSA patches to deal with pulseaudio issues (#49826)

* Fri Apr 10 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29.1-2mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Disable CONFIG_AES2501 (#40523)
    - Hide unused interface in option for D-Link DWM-652 and ensure it is ignored
      by usb-storage when in modem mode

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Disable gem automatically if it's not possible to do tiled
      rendering, fixes 3d performance regression on some intel i945
      based machines. Fix/patch made by Ander Conselvan de Oliveira.
      With this remove previous gem_enable parameter added to i915,
      obsolete by this solution.
    - rt2x00: prevent double kfree when failing to register hardware
      (#46710).
    - Enable and select minstrel as default mac80211 rate control
      (should behave better than previous pid, 2.6.29 default).

* Tue Apr 07 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29.1-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Enabled CONFIG_X86_GENERICARCH for all i386 configs, as we set
      NR_CPUS=32 (reported by Pascal Terjan).
    - Disabled CONFIG_WIRELESS_OLD_REGULATORY on all configs.
    - Disabled CONFIG_USB_GADGET on configs where it was enabled.
    - Tomoyo update to 1.6.7-20090401
    - Added parameter gem_enable to i915, based on patch/idea posted by
      Vasily Khoruzhick, for more information see following bug report:
      http://bugs.freedesktop.org/show_bug.cgi?id=16835
    - Refresh gpu-drm-radeon-r6xx-r7xx.patch with following additional
      commits:
      radeon: add some new pci ids
      drm/radeon: load the right microcode on rs780
    - Removed pat cleanup (new vm flag to track full pfnmap at mmap),
      keep with 2.6.29 stable series default.
    - elantech: apply upstream patch with workaround for jumpy cursor on
      firmware 2.34
    - Add via card reader support (sd/mmc only) v5 patch from Joseph
      Chan.
    - Removed already applied patches:
      input-add-dell-xps-m1530-nomux-quirk.patch
      net-sis190-sis966.patch (similar fix merged)
      net-bluetooth-fix-oops-in-l2cap_conn_del.patch
      net-bluetooth-fix-esco-sync.patch (similar fix merged)
    - scripts/apply_patches: use --fuzz=0 for patch (same default as for
      general distro packages).
    - Rediffed all fuzzy patches. Some styling/trailing spacing removal
      fixes were done too.
    - Drop x86-cpufreq-e_powersaver-print-voltage-mult-only-in-debug.patch,
      stick with upstream default after change "[CPUFREQ] Remove
      debugging message from e_powersaver".
    - Renamed acpi-CELVO-M360S-disable_acpi_irq.patch to
      acpi-CLEVO-M360S-disable_acpi_irq.patch, and rediffed.
    - Removed unecessary patches:
      net-bonding-alias.patch (possible easter egg? :-) )
      usb-use-old_scheme_first.patch
    - Updated acpi-dsdt-initrd patch with enhanced/fixed version.
      (version v0.9c-2.6.28). Added more fixes on top of updated patch.
    - Updated ipset to 2.4.9 (matches current userspace on cooker, and
      fixes oops when running ipset tests).

  o Pascal Terjan <pterjan@mandriva.com>
    - Add support for Wacom Intuos 4 tablets (based on linuxwacom cvs patches)
    - Add support for D-Link DWM 652 3G modem

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.29.1
    - update drbd to 8.3.1

* Thu Mar 26 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Backported r6xx/r7xx support from drm-next tree.
    - Updated to 2.6.29
      * dropped following merged patches:
        fs-ext4-fix-header-check-in-ext4_ext_search_right-fo.patch
        fs-ext4-Print-the-find_group_flex-warning-only-once.patch
    - Included x86 pat fixes, should fix problems reported at kernel.org
      bug #12800, and fixes virtualbox regression without the workaround
      setting VBOX_USE_INSERT_PAGE=1
      Reference: http://www.virtualbox.org/ticket/3403
    - Added bug fix for network stuck issue in 2.6.29 final
      Reference: http://marc.info/?l=linux-kernel&m=123789980524715&w=2

* Wed Mar 18 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29-0.rc8.3.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Rediff main uss725 patch, fixes In-System Design USS725 USB/IDE
      probe error reported by Sergio Monteiro Basto.
    - Select default CONFIG_SCTP_HMAC_MD5 on all configs (instead of
      CONFIG_SCTP_HMAC_NONE currently selected).
    - Disabled CONFIG_SYS_DEPRECATED* on all configs, report/reference:
      http://lists.mandriva.com/kernel-discuss/2009-03/msg00036.php
    - Disabled CONFIG_USB_DEVICE_CLASS on all configs, report/reference:
      http://lists.mandriva.com/kernel-discuss/2009-03/msg00037.php
    - Updated to 2.6.29-rc8-git3

* Fri Mar 13 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29-0.rc8.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - mac80211: deauth before flushing STA information.
      (handles mac80211 userspace notification issue when interface goes
      down pointed at ticket #43441).
    - Enabled (=y) on all kernel configs: CONFIG_CPU_FREQ_STAT_DETAILS,
      CONFIG_IPV6_ROUTER_PREF, CONFIG_IPV6_ROUTE_INFO,
      CONFIG_IPV6_OPTIMISTIC_DAD, CONFIG_IPV6_MROUTE,
      CONFIG_IPV6_PIMSM_V2.
    - Enabled cpufreq options on powerpc config.
    - Enabled CONFIG_TCP_MD5SIG on server kernels.
    - Updated to 2.6.29-rc8
    - Included following ext4 fixes from Theodore Ts'o git tree:
      * Fixes for 2.6.29-rcX:
      ext4: fix header check in ext4_ext_search_right() for deep extent trees
      ext4: Print the find_group_flex() warning only once
      * ext4+delayed allocation issues solution (reference:
      http://thunk.org/tytso/blog/2009/03/12/delayed-allocation-and-the-zero-length-file-problem/)
      ext4: add EXT4_IOC_ALLOC_DA_BLKS ioctl
      ext4: Automatically allocate delay allocated blocks on close
      ext4: Automatically allocate delay allocated blocks on rename

* Tue Mar 10 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29-0.rc7.4.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Disabled on all kernel configs: CONFIG_MTD_PHYSMAP,
      CONFIG_MTD_PLATRAM, CONFIG_MTD_NAND_PLATFORM,
      CONFIG_PARPORT_AX88796, CONFIG_RTC_DRV_DS1286,
      CONFIG_RTC_DRV_DS1511, CONFIG_RTC_DRV_DS1672,
      CONFIG_RTC_DRV_FM3130, CONFIG_RTC_DRV_M48T35,
      CONFIG_RTC_DRV_M48T86, CONFIG_RTC_DRV_MAX6900,
      CONFIG_RTC_DRV_PCF8583, CONFIG_RTC_DRV_S35390A,
      CONFIG_RTC_DRV_STK17TA8, CONFIG_RTC_DRV_TEST,
      CONFIG_RTC_DRV_X1205, CONFIG_UIO_PDRV,
      CONFIG_UIO_PDRV_GENIRQ, CONFIG_UIO_SMX,
      CONFIG_LCD_PLATFORM, CONFIG_FB_METRONOME.
    - Enabled (=m) on sparc config: CONFIG_PARPORT_SUNBPP,
      CONFIG_VIDEO_WM8775, CONFIG_SND_MTPAV, CONFIG_SND_PORTMAN2X4,
      CONFIG_SND_SERIAL_U16550.
    - Enabled (=y) on x86_64 config: CONFIG_PARPORT_PC_SUPERIO,
      CONFIG_DIRECT_GBPAGES.
    - Enabled (=y) on i386/x86_64 configs: CONFIG_SONYPI_COMPAT,
      CONFIG_PM_DEBUG, CONFIG_PM_TRACE_RTC.
    - Change from =m to =y CONFIG_RTC_CLASS/CONFIG_RTC_LIB on powerpc
      config.
    - Disabled on i386/powerpc/x86_64 configs: CONFIG_RTC_DRV_BQ4802,
      CONFIG_RTC_DRV_M48T59, CONFIG_USB_GPIO_VBUS, CONFIG_USB_OTG_UTILS.
    - Enabled (=y) on sparc/powerpc configs:
      CONFIG_RTC_INTF_DEV_UIE_EMUL.
    - Disabled on i386/x86_64 configs: CONFIG_RTC_DRV_DS1307,
      CONFIG_RTC_DRV_DS1553, CONFIG_RTC_DRV_DS1742,
      CONFIG_RTC_DRV_V3020, CONFIG_FB_N411, CONFIG_FB_HECUBA,
      CONFIG_FB_VIRTUAL.
    - Enabled (=m) on powerpc config: CONFIG_RTC_DRV_DS1307,
      CONFIG_RTC_DRV_DS1742.
    - Disabled on i386/sparc/x86_64 configs: CONFIG_RTC_DRV_DS1374,
      CONFIG_RTC_DRV_M41T80, CONFIG_RTC_DRV_PCF8563,
      CONFIG_RTC_DRV_RS5C372, CONFIG_RTC_DRV_RX8581,
      CONFIG_FB_S1D13XXX.
    - Enabled (=m) on sparc/powerpc configs: CONFIG_VIDEO_CX88*,
      CONFIG_RTC_DRV_ISL1208.
    - Disabled on sparc/powerpc configs: CONFIG_RTC_INTF_PROC,
      CONFIG_LCD_CLASS_DEVICE.
    - Enabled (=y) on sparc config: CONFIG_SERIAL_8250_EXTENDED,
      CONFIG_SERIAL_8250_SHARE_IRQ.
    - Enabled (=y) on all configs: CONFIG_SERIAL_8250_RSA.
    - Enabled (=m) on i386 config: CONFIG_FB_ARC, CONFIG_EFI_VARS.
    - Enabled (=y) on i386 config: CONFIG_EFI, CONFIG_FB_EFI,
      CONFIG_FB_HGA_ACCEL.
    - n411: add missing Makefile entry.
    - Disabled on x86_64 config: CONFIG_FB_HGA.
    - Enable group cpu scheduler, switch to cgroup scheduler on server
      config.
    - Only enable namespaces support for server config.
    - Only enable (=m) virtual ethernet pair device and MAC-VLAN for
      server config.
    - Fixes/enhancements for HP Educ.ar machine/alc888 3stack-hp model:
      * Added additional 4 channel mode
      * Added headphone automute support
      * Map 3stack-hp model (ALC888) for HP Educ.ar
    - ALSA: hda - Cleanup printk from alc888_6st_dell_unsol_event
    - Updated to 2.6.29-rc7-git4
      * dropped w1-slaves-ds2431-kbuild.patch (merged)
    - Turn on DEVPTS_MULTIPLE_INSTANCES for server kernels.
    - Enable Xen guest support by default when available.
    - create_configs: cleanup unused/gone config options, cosmetics,
      enable xen when available (not only when customizing options for
      server kernel).

  o Bogdano Arendartchuk <bogdano@mandriva.com.br>
    - Keep Module.symvers as /boot/symvers-$version.gz in order to allow
      partial kernel builds

* Tue Feb 24 2009 Pascal Terjan <pterjan@mandriva.com> 2.6.29-rc6.1.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Tomoyo build patch update for 2.6.29-rc5
    - Disabled on all kernel configs: CONFIG_USB_R8A66597_HCD,
      CONFIG_PATA_PLATFORM, CONFIG_I2C_GPIO, CONFIG_I2C_OCORES,
      CONFIG_I2C_SIMTEC, CONFIG_I2C_PCA_PLATFORM, CONFIG_I2C_STUB,
      CONFIG_BLK_DEV_PLATFORM, CONFIG_KEYBOARD_GPIO, CONFIG_MOUSE_GPIO,
      CONFIG_LEDS_GPIO, CONFIG_LEDS_PCA9532, CONFIG_LEDS_PCA955X.
    - Disabled on powerpc config: CONFIG_I2C_ISCH.
    - Disabled on sparc config: CONFIG_I2C_ALI1535, CONFIG_I2C_ALI1563,
      CONFIG_I2C_ALI15X3, CONFIG_I2C_AMD756, CONFIG_I2C_AMD8111,
      CONFIG_I2C_I801, CONFIG_I2C_ISCH, CONFIG_I2C_NFORCE2,
      CONFIG_I2C_PIIX4, CONFIG_I2C_SIS5595, CONFIG_I2C_SIS630,
      CONFIG_I2C_SIS96X, CONFIG_I2C_VIA, CONFIG_I2C_VIAPRO.
    - Enabled on powerpc config: CONFIG_COMPUTONE,
      CONFIG_I2C_VOODOO3, CONFIG_LEDS_TRIGGER_TIMER,
      CONFIG_LEDS_TRIGGER_HEARTBEAT.
    - Disabled on x86_64 config: CONFIG_LEDS_ALIX2.
    - Enabled on sparc config: CONFIG_NEW_LEDS, CONFIG_LEDS_CLASS,
      CONFIG_LEDS_SUNFIRE, CONFIG_LEDS_TRIGGERS*.

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.29-rc6-git1
    - add drivers/acpi/acpica header files to -devel rpms, needed by fglrx

* Fri Feb 20 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29-0.rc5.4.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - ALSA/hda changes:
      * Include new SND_PCI_QUIRK_MASK and SND_PCI_QUIRK_VENDOR macros,
        cleanup IDT92HD7x HP quirks and backport SND_PCI_QUIRK_MASK
        cleanup for stac922x ecs202 model from alsa tiwai's sound tree.
      * Fix speaker output on HP DV4 1155-SE
    - Disabled on all kernel configs: CONFIG_MDIO_BITBANG,
      CONFIG_MDIO_GPIO, CONFIG_UCB1400_CORE, CONFIG_TOUCHSCREEN_ADS7846,
      CONFIG_TOUCHSCREEN_WM97XX, CONFIG_TOUCHSCREEN_TSC2007, CONFIG_SPI,
      CONFIG_MFD_WM8350_I2C, CONFIG_W1_MASTER_GPIO,
      CONFIG_W1_SLAVE_BQ27000, CONFIG_W1_SLAVE_DS2760,
      CONFIG_BATTERY_BQ27x00, CONFIG_BATTERY_DS2760, CONFIG_PDA_POWER,
      CONFIG_SENSORS_ADS7828, CONFIG_HTC_PASIC3, CONFIG_MFD_SM501,
      CONFIG_TPS65010, CONFIG_MFD_WM8400, CONFIG_SOC_CAMERA,
      CONFIG_USB_C67X00_HCD, CONFIG_USB_ISP116X_HCD.
    - Disabled on x86_64 config: CONFIG_TOUCHSCREEN_MK712.
    - Disabled on powerpc config: CONFIG_TOUCHSCREEN_TOUCHIT213.
    - Disabled on powerpc/sparc: CONFIG_HWMON_VID, CONFIG_SENSORS_AD*,
      CONFIG_SENSORS_F718*, CONFIG_SENSORS_F75375S,
      CONFIG_SENSORS_LTC4245, CONFIG_SENSORS_MAX*,
      CONFIG_SENSORS_W83792D, CONFIG_SENSORS_W83L786NG,
      CONFIG_SENSORS_DS1621, CONFIG_SENSORS_I5K_AMB,
      CONFIG_SENSORS_GL5*, CONFIG_SENSORS_IT87, CONFIG_SENSORS_LM*,
      CONFIG_SENSORS_PC87360, CONFIG_SENSORS_SIS5595,
      CONFIG_SENSORS_DME1737, CONFIG_SENSORS_SMS*,
      CONFIG_SENSORS_THMC50, CONFIG_SENSORS_VIA686A,
      CONFIG_SENSORS_W83781D, CONFIG_SENSORS_W83L785TS,
      CONFIG_SENSORS_W83627HF.
    - Enabled (=m) on powerpc config: CONFIG_TOUCHSCREEN_ELO,
      CONFIG_TOUCHSCREEN_MTOUCH, CONFIG_TOUCHSCREEN_PENMOUNT,
      CONFIG_TOUCHSCREEN_TOUCHRIGHT, CONFIG_TOUCHSCREEN_TOUCHWIN.
    - w1: add missing Kconfig/Makefile entries for DS2431 slave driver.
    - Updated to 2.6.29-rc5-git4
      * fixed drbd build with BIO_RW_SYNC change.

  o Bogdano Arendartchuk <bogdano@mandriva.com.br>
    - Enabled CONFIG_MODVERSIONS and CONFIG_MODULE_SRCVERSION_ALL, as a
      first step towards ABI control

* Mon Feb 16 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.29-0.rc5.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Updated to 2.6.29-rc5
      * Removed following merged patches:
        x86-cpufreq-add-more-pcore-fsbs.patch
        x86-cpufreq-add-celeron-core-to-p4-clockmod.patch
        char-agp-intel-agp-add-support-for-G41-chipset.patch
        fs-squashfs3.4.patch
        fs-squashfs3.4-2.6.28.patch
        media-video-uvc-add-support-for-samsung-q310-webcam.patch
        media-video-uvc-add-support-for-thinkpad-sl500-webcam.patch
        media-video-uvc-sort-the-frame-descriptors-during-parsing.patch
        media-video-uvc-handle-failed-GET_MIN_MAX_DEF-more-gracefully.patch
        media-video-uvc-commit-stream-param-when-enabling-stream.patch
        misc-eeepc-laptop-check-return-values-from-rfkill_register.patch
        misc-eeepc-laptop-implement-rfkill-hotplugging-in-eeepc-laptop.patch
        misc-eeepc-laptop-add-support-for-extended-hotkeys.patch
        net-fix-userland-breakage-wrt-if_tunnel.h.patch
        serial-RS485-ioctl-structure-uses-__u32-include.patch
        sound-alsa-hda-Add-quirk-for-another-HP-dv5-model.patch
        btusb-add-broadcom-dongle.patch
      * Rediffed/Redid following patches:
        acpi-add-proc-event-regs.patch
        fs-dynamic-nls-default.patch
        media-dvb-add-Yuan-PD378S.patch
        serial-docomo-F2402.patch
        sound-alsa-hda-add-acer-alc889-model.patch
        sound-alsa-hda-92hd71xxx-disable-unmute-support-for-code.patch
        sound-alsa-hda-Additional-pin-nids-for-STAC92HD71Bx-and.patch
        sound-alsa-hda-Dynamic-detection-of-dmics-dmuxes-smuxes.patch
        sound-alsa-hda-Don-t-call-stac92xx_parse_auto_config-wi.patch
        sound-alsa-hda-one-more-hp-dv7-quirk.patch
        sound-alsa-hda-Don-t-touch-non-existent-port-f-on-4-por.patch
        sound-alsa-hda-sigmatel-ecs202-new-quirk.patch
        usb-storage-uss725-build-fixes.patch
        bluetooth-hci_usb-disable-isoc-transfers.patch
        hid-usbhid-quirk-multilaser.patch
        3rd-3rdparty-merge.patch
      * Pending/moved to patches-broken:
        - acpi-asus-input.patch: same functionality merged upstream, but
          needs extra checking on some extra/different key codes to be
          dropped.
        - hid-hotplug-racefix.patch: possibly fixed by commit "HID:
          hiddev cleanup -- handle all error conditions properly"
          upstream.
      * Dropped from patches-broken:
        - media-video-uvc-max-iso-pkts.patch: no machine/environment
          available anymore to reproduce the problem.
      * Added alc889 fixes submitted upstream for which
        sound-alsa-hda-add-acer-alc889-model.patch depends:
        sound-alsa-hda-consider-additional-capsrc-alc889.patch
        sound-alsa-hda-alc882_auto_init_input_src-selector.patch 
      * Updated tomoyo to 1.6.6-20090202, 2.6.29-rc3 build and kernel
        log warning patches adapted.
      * Adjusted drbd and unionfs for 2.6.29 changes.
      * Removed rt2860 from additional 3rdparty drivers, it is now
        included in staging.
      * Update ipt_set for netfilter/xtables changes in 2.6.29
    - ALSA/hda/idt: change HP dv7 (103c:30f4) quirk from hp-m4 to hp-dv5
      model, to fix not working internal microphone. References:
      https://qa.mandriva.com/show_bug.cgi?id=44855#c193
      https://qa.mandriva.com/show_bug.cgi?id=44855#c196
    - Fixed build warnings in agnx and rtl8187se staging drivers.

  o Anssi Hannula <anssi@mandriva.org>
    - Disable CONFIG_HID_COMPAT (hid-dummy module) as our udev supports
      driver autoloading on all buses.

  o Thomas Backlund <tmb@mandriva.org>
    - update drbd to 8.3.0

* Mon Feb 09 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.28.4-1mnb
  o Anssi Hannula <anssi@mandriva.org>
    - Build HID core as modules instead of built-in. Having it built-in
      makes no sense as both USB HID and Bluetooth HIDP are built as
      modules anyway.

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Remove previous applied enhancements/fixes to STAC92HD71Bx and
      STAC92HD75Bx hda codec support, and reapply splitted changes
      submitted upstream. Apply also additional fixes and HP dv quirks
      in sound tree. Added additional quirk for HP dv7 to be submitted
      after I get positive report about it.
    - ALSA/hda: Map new ecs motherboard id 1019:2950 to STAC9221 ecs202
      model.
    - Updated to 2.6.28.4
      * removed input-samsung-nc10.patch (merged)

* Wed Feb 04 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.28.3-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Updated to 2.6.28.3
      * removed x86-pat-1MB-nonram.patch (merged)
    - Added upstream fixes for the exported userspace headers (build
      with linux/ip.h and linux/serial.h bugs). References:
      http://lists.mandriva.com/kernel-discuss/2009-02/msg00000.php
      https://qa.mandriva.com/show_bug.cgi?id=47313

* Wed Jan 28 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.28.2-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Updated to 2.6.28.2
      * removed following patches (already applied or obsolete with
        "usb-storage: set CAPACITY_HEURISTICS flag for bad vendors"
        change):
        usb-storage-unusual_devs-nokia-5200.patch
        usb-storage-unusual-devs-nokia-5610.patch
      * rediff sound-alsa-hda-enhance_fix_stac92hd71bx_stac92hd75bx.patch
      * cosmetic changes at sound-alsa-hda-add-acer-alc889-model.patch
    - Updates for sreadahead 1.0 support.

* Fri Jan 23 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.28.1-2mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Fix snd-hda-intel oops with some alc883 models after addition of
      model for Acer Aspire 8930 in previous release.

* Thu Jan 22 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.28.1-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Add Suggests for crda in kernel packages.
    - Updated to 2.6.28.1
    - Add MSI quirk list for hda devices, to force enable_msi setting
      parameter when needed (#44855).
    - Enhance/fix some aspects related to STAC92HD71Bx and STAC92HD75Bx
      support (#44855).
    - Add hda-intel ALC889 model for Acer Aspire 8930 (#45838).

  o Pascal Terjan <pterjan@mandriva.com>
    - Disable asus_acpi, we have asus-laptop and eeepc-laptop
    - Add back patch on asus-laptop to convert acpi events to input
      * Update it for 2.6.28
      * Emit the acpi event when the key is unknown
    - Add id for Yuan PD378S DVB receiver (from Arnaud)

* Wed Jan 14 2009 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.28-3mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Add patch from upstream #12372 to allow X starting on some
      systems (#46384)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update configs to 2.6.28: CONFIG_X86_PTRACE_BTS is being disabled because
      it's marked as broken and as CONFIG_X86_DS depends on it it's also being
      disabled
    - Make CONFIG_IDE modular in all configs (asked by Thierry Vignaud)
    - Fix rtc-cmos loading on x86_64 machines (patch suggested by Oden Eriksson)

* Tue Dec 30 2008 Pascal Terjan <pterjan@mandriva.com> 2.6.28-2mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Support fn+* in Samsung NC10 

* Mon Dec 29 2008 Pascal Terjan <pterjan@mandriva.com> 2.6.28-1mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Updated to 2.6.28 final

* Fri Dec 12 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.28-0.rc8.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Updated to 2.6.28-rc8
      * Dropped (merged):
        x86-add-northbridge-pci-ids-for-fam-0x11-processors.patch
        x86-add-detection-of-AMD-family-0x11-northbridges.patch
        fastboot-1.patch
        acpi-add-preemption-to-avoid-latency-issue.patch
        acpi-ACPICA-Add-function-to-dereference-returned-referen.patch
        ata-ata_piix-hercules-ec900-short-cable.patch
        ide-pci-piix-hercules-ec900-short-cable.patch
        scsi-megaraid-proc-oops.patch
        gpu-drm-SiS-DRM-fix-a-pointer-cast-warning.patch
        gpu-drm-fix-sysfs-error-path.patch
        gpu-drm-radeon-fix-writeback-across-suspend-resume.patch
        gpu-drm-i915-remove-settable-use_mi_batchbuffer_start.patch
        gpu-drm-i915-Ignore-X-server-provided-mmio-address.patch
        gpu-drm-i915-Use-more-consistent-names-for-regs-and-store.patch
        gpu-drm-i915-Add-support-for-MSI-and-interrupt-mitigation.patch
        gpu-drm-i915-Track-progress-inside-of-batchbuffers-for-dete.patch
        gpu-drm-Add-Intel-ACPI-IGD-OpRegion-support.patch
        gpu-drm-i915-save-restore-MCHBAR_RENDER_STANDBY.patch
        media-video-uvc-implement-usb-reset-resume.patch
        media-video-uvc-supress-spurious-EOF-in-empty-payload-trace-msg.patch
        media-video-uvc-fix-incomplete-frame-drop-switch-variable-size.patch
        media-video-uvc-dont-use-part-of-buffer-for-USB-transfer.patch
        media-video-uvc-declare-missing-unit-controls.patch
        media-video-uvc-control-cache-access-fix.patch
        media-video-uvc-add-bison-quirk-fujitsu-amilo-si2636.patch
        media-video-uvc-add-bison-quirk-advent-4211.patch
        media-video-uvc-support-two-new-bison-webcams.patch
        media-video-gspca-add-m5602-driver.patch
        misc-add-panasonic-laptop-extras.patch
        net-sis190-add-atheros-phy-ar8012.patch
        net-r8169-Tx-performance-tweak-helper.patch
        net-r8169-use-pci_find_capability-for-the-PCI-E-feature.patch
        net-r8169-add-8168-8101-registers-description.patch
        net-r8169-add-hw-start-helpers-for-the-8168-and-the-810.patch
        net-r8169-additional-8101-and-8102-support.patch
        net-r8169-WoL-fixes-part-1.patch
        net-r8169-WoL-fixes-part-2.patch
        net-wireless-b43-Fix-QoS-defaults.patch
        net-wireless-b43legacy-Fix-to-enhance-TX-speed.patch
        net-wireless-b43-Fix-Bluetooth-SPROM-coding-error-Motorola-7010-BCM4306.patch
        net-atl2-add-atl2-driver.patch
        net-atl2-add-tx-bytes-statistic.patch
        net-enic-add-Cisco-10G-Ethernet-NIC-driver.patch
        net-enic-Don-t-indicate-IPv6-pkts-using-soft-LRO.patch
        net-enic-fixes-for-review-items-from-Ben-Hutchings.patch
        net-enic-Bug-fix-Free-MSI-intr-with-correct-data-handl.patch
        net-enic-bug-fix-don-t-set-netdev-name-too-early.patch
        net-jme-JMicron-Gigabit-Ethernet-Driver.patch
        net-qlge-New-Qlogic-10Gb-Ethernet-Driver.patch
        net-qlge-Fix-warnings-in-debugging-code.patch
        net-qlge-Protect-qlge_resume-with-CONFIG_PM.patch
        net-bluetooth-apple-wireless-keyboard-fnkey.patch
        net-wireless-iwlagn-downgrade-BUG_ON-in-interrupt.patch
        sound-alsa-revert-for-20081011-merge.patch
        sound-alsa-20081011-merge.patch
        sound-alsa-20081013-merge.patch
        sound-alsa-20081016-merge.patch
        sound-alsa-20081017-merge.patch
        sound-alsa-20081020_1-merge.patch
        sound-alsa-20081020_2-merge.patch
        sound-alsa-20081020_3-merge.patch
        sound-alsa-20081023-merge.patch
        sound-alsa-20081027-merge.patch
        sound-alsa-pci_ioremap_bar-only-in-2.6.28.patch
        sound-alsa-revert-for-20081030-merge.patch
        sound-alsa-20081030-merge.patch
        sound-alsa-20081103-merge.patch
        sound-alsa-20081110-merge.patch
        sound-alsa-20081112-merge.patch
        sound-alsa-20081118-merge.patch
        sound-alsa-20081130-merge.patch
        usb-storage-nokia-6300.patch
        usb-storage-unusual-devs-nokia-7610.patch
      * Moved to patches-broken:
        irq-debug-shared.patch
        pci-default-nomsi.patch (continue to disable msi by default?)
        scsi-sg-allow-dio-as-default.patch
        hwmon-applesmc-retry-when-accessing-keys.patch (still needed?)
        hwmon-applesmc_int.patch (useful?)
        media-video-uvc-max-iso-pkts.patch
        apparmor patches
        aufs patches
      * Redid/Rediffed following patches (because of broken apply,
        broken build or other updates for 2.6.28):
        ide-pci-sis5513-965.patch
        fs-dynamic-nls-default.patch
        media-video-uvc-handle-failed-GET_MIN_MAX_DEF-more-gracefully.patch
        net-netfilter-psd-mdv.patch
        hid-usbhid-IBM-BladeCenterHS20-quirk.patch
        hid-usbhid-quirk-multilaser.patch
        3rd-3rdparty-merge.patch
        gpu-drm-mach64.patch
        gpu-drm-mach64-fixes.patch
        net-netfilter-IFWLOG-mdv.patch
        net-netfilter-psd-mdv.patch
      * Update ipt_set for netfilter/xtables changes in 2.6.28
      * Removed kernel-add-mute-events-log-level.patch (not worth/sent
        upstream).
      * Removed fastboot-2.patch (asynchronous stuff not accepted
        into 2.6.28).
      * Removed acpi-asus-laptop-input.patch and acpi-eeepc-input.patch,
        as different input support was merged for eeepc-laptop.
      * Removed net-enic-build-fix.patch, not needed on 2.6.28
      * Removed acpi-dsdt-initrd-fastboot.patch, not needed anymore.
      * Removed net-wireless-at76_usb.patch, at76_usb is now in staging
        tree.
      * Updated drbd code for 2.6.28 (3rd-drbd-2.6.28.patch).
      * Added patch from squashfs CVS to allow successful build on 2.6.28
      * Removed 3rdparty prism25 and et131x which are now in staging.

* Fri Dec 05 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.7-3mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Changes to eeepc-laptop based on changes made by Matthew Garrett
      and posted on LKML:
      * Backport wireless hotplug support for eeepc-laptop on 2.6.27
        from http://lkml.org/lkml/2008/11/17/170 (#43332).
      * acpi-eeepc-input.patch: add more hotkeys for newer eeepc models,
        keycode references from http://lkml.org/lkml/2008/11/17/161
    - Upstream alsa bug fixes/updates (1.0.18, 20081130 merge).

  o Pascal Terjan <pterjan@mandriva.com>
    - Enable CONFIG_CIFS_DFS_UPCALL

* Wed Nov 26 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.7-2mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Support for broadcom bluetooth dongle 0a5c:2009 in btusb (#44886)

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Sync alsa/uvc updates with kernel-2.6.27-0.uc1mnb2 available in
      main/testing for 2009.0

* Tue Nov 25 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.7-1mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Disable CONFIG_BLK_DEV_UB (#45599)

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Update to 2.6.27.7 (CVE-2008-5033)
      * dropped input-ALPS-add-signature-for-DualPoint-model-found-in-Dell-Latitude-E6500.patch
        (merged)
    - Apply upstream workaround for #44891 (iwlagn: downgrade BUG_ON in
      interrupt).
    - Backport gspca m5602 driver from 2.6.28 (#44898).
    - Add fix for ppscsi module oops (#45393).

* Sat Nov 15 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.6-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Include r8169 WoL fixes from 2.6.28, related ticket: #41782
    - i915/drm: backported bug fix for suspend/resume with i915 on some
      configurations (Save/restore MCHBAR_RENDER_STANDBY commit on
      2.6.28).
    - Update to 2.6.27.6
      * dropped md-fix-bug-in-raid10-recovery.patch (merged)
      * dropped net-r8169-get-ethtool-settings-through-the-generic-mii.patch
        (merged)
      * dropped net-wireless-iwlwifi-generic-init-calibrations-framework.patch
        (merged)
      * dropped security-keys-request_key-oops.patch (merged)
    - More alsa 1.0.18 updates, snd-hda-intel sigmatel codec fixes
      among others.
    - unusual_ids usb-storage addition for Nokia XpressMusic 5200
      (#44988).
    - More unusual_devs additions for Nokia 5610/7610 (sources:
      linux-usb ML and Ubuntu bug #287701).

  o Pascal Terjan <pterjan@mandriva.com>
    - Enable the Nokia 6300 quirk for new revisions

* Sun Nov 09 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.5-1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Fix eeepc shutdown hang caused by snd-hda-intel (#44752)

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Backport uvcvideo fixes from 2.6.28 and linux-uvc svn.
    - Update to 2.6.27.5
      * dropped acpi-ec-fast-transaction.patch (merged)
      * rediffed char-agp-intel-agp-add-support-for-G41-chipset.patch
      * dropped net-restore-ordering-of-tcp-options.patch (merged)
      * dropped sound-alsa-snd-hda-intel-fix-halt-hang.patch (merged)
    - Alsa updates from 2.6.27-git* (2.6.28).
      * fixed Realtek auto-mute bug (#45618)
    - Apply upstream change in acpi "ACPICA: Add function to dereference
      returned reference objects" (#44870).
    - Fix pcspkr disabled in kernel configs (#45319).
    - Add patch to fix oops in prism2_usb (#44612).

  o Thomas Backlund <tmb@mandriva.org>
    - fix drbd CN_IDX 0x4 conflict with v86d
    - fix md raid10 recovery bug

* Tue Oct 28 2008 Pascal Terjan <pterjan@mandriva.com> 2.6.27.4-2mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Fix a oops in request_key when keyring is not already there
      (Happens when mounting CIFS with kerberos)

* Mon Oct 27 2008 Pascal Terjan <pterjan@mandriva.com> 2.6.27.4-1mnb
  o Pascal Terjan <pterjan@mandriva.com>
     - Fix a oops when reading /proc/megaraid/hba0/diskdrives-ch* (upstream #11792)
     - Add Fastboot patches (raid auto detection is now off by default, you can
       enable it with raid=autodetect boot option)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
     - Update to 2.6.27.4
       * Drop usb-atm-speedtch-2.6.27-fix.patch (merged)
     - Restore ordering of TCP options (#43372)

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
     - Alsa fixes from 2.6.27-git* (2.6.28).

* Wed Oct 22 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.3-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Update to 2.6.27.3
    - More alsa updates from 2.6.27-git* (2.6.28).

* Wed Oct 22 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.2-3mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update .configs
    - Fix USB ATM Speed Touch OOPS (#44803)

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Don't install vmlinux as executable for debug packages to avoid
      strip_and_check_elf_files from spec-helper stripping it.

* Mon Oct 20 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.2-2mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Update alsa 1.0.18rc3 to "final" version included in kernel 2.6.28
      and dropped following patches:
      * sound-alsa-revert-fixes.patch (not needed anymore)
      * sound-hda-codec-add-Foxconn-45CMX_45GMX_45CMX-K-quirk.patch
        (merged)
      * sound-hda-codec-fix-ALC662-auto-config-mixer-mutes.patch
        (merged)
      * sound-hda-codec-slave_dig_outs-oops.patch (merged)
      * sound-hda-codec-add-Gigabyte-945GCM-S2L-quirk.patch (merged)

  o Pascal Terjan <pterjan@mandriva.com>
    - Drop Acer One alsa quirk, it works now better with "auto" model

* Sat Oct 18 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.2-1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Enable CONFIG_KPROBES: needed for systemtap

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Create kernel debug packages with vmlinux and debugging symbols
      from modules.
    - Disable CONFIG_KALLSYMS_EXTRA_PASS were it was enabled, as Kconfig
      description states this should only be enabled temporarily as a
      workaround while something is broken in kallsyms.
    - Update to 2.6.27.2
      * dropped net-wireless-b43legacy-Fix-failure-in-rate-adjustment-mechanism.patch
        (merged)
      * dropped net-wireless-libertas-clear-current-command-on-card-removal.patch
        (merged)

* Fri Oct 10 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Add i8042_nomux quirk for Dell XPS M1530 (#43532).
    - Merge enic, qlge and atl2 fixes from net-next tree.
    - Add p4-clockmod support for Celeron Core processors (#43885).
    - Add Panasonic Let's Note laptop extras driver from acpi-test. Now
      dkms-pcc-acpi packages can be dropped.
    - Added superreadahead ext3 patch for tests to be done with it.

  o Pascal Terjan <pterjan@mandriva.com>
    - Update to 2.6.27 final
      * Drop x86-enable_mtrr_cleanup-early-boot-param-typo-fix.patch (merged)
      * Drop accessibility-braille-really-disable-by-default.patch (merged)
      * Drop net-e1000e-write-protect-ICHx-NVM-to-prevent-malicious-write_erase.patch
        (merged)

* Wed Oct 01 2008 Pascal Terjan <pterjan@mandriva.com> 2.6.27-0.rc8.2mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Add fix for e1000e corruption bug and re-enable it
      (http://lkml.org/lkml/2008/10/1/368). Closes #44147

* Wed Oct 01 2008 Pascal Terjan <pterjan@mandriva.com> 2.6.27-0.rc8.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Fix sis190 ethernet device support on Asus P5SD2-VM motherboard
      (kernel.org bug #11073).
    - Add fix for sata_nv regression in latest 2.6.27 rcs (kernel.org
      bug #11615). Closes: #44287
    - Remove 3rdparty acx driver due to its dubious legal status
      (unanswered questions about reverse engineering process done while
      developing the driver).
    - Enable CONFIG_KARMA_PARTITION, otherwise Rio Karma mp3 player is
      unusable.
    - drbd fixes for Linux 2.6.27
    - 3rdparty/rt2860: Fix x86_64 issues found while inspecting x86_64
      build logs.
    - Add patch from LKML titled "Input: ALPS - add signature for
      DualPoint model found in Dell Latitude E6500" from Elvis
      Pranskevichus, reported/requested by Frederik Himpe.
    - Fix typo in early boot parameter that enables mtrr cleanup, patch
      from J.A. Magallon.
    - p4-clockmod: set reasonable default for scaling_min_freq, to
      prevent too low performance with governors that use the lowest
      frequency. Closes: #43155

  o Pascal Terjan <pterjan@mandriva.com>
    - Update to 2.6.27-rc8

* Sat Sep 27 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27-0.rc7.5.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Drop acpi-tc1100-wmi* patches, kernel already has all relevant
      support.
    - patches-broken: rediff and fix hid-usbhid-IBM-BaldeCenterHS20-HID.patch
      for 2.6.27 (rename also to hid-usbhid-IBM-BladeCenterHS20-quirk.patch)
    - Include patch from linux-acpi to avoid stalls while inside acpi
      code in slow machines, like when reading acpi battery info
      (http://marc.info/?l=linux-acpi&m=122235488029621&w=2). A
      workaround could be used too for the problem, using cache_time
      parameter of battery module setting a larger value, but the patch
      to preempt acpi code is a better/definitive solution.
    - Add again Intel ACPI IGD OpRegion support patch and its needed
      patches, but now without the patch that introduced the regression
      found with one 855GM based laptop (the patch that introduced the
      regression was "i915: Initialize hardware status page at device
      load when possible.", turned out also that this patch wasn't
      really needed in the series so it's safely dropped). Closes: #43061
    - Drop Wacom ACPI patches: seems they were forgotten here, same
      functionality should already be provided by drivers/serial/8250_pnp.c
    - ALSA/hda-intel: map proper ALC662 model for Gigabyte 945GCM-S2L
      and Foxconn 45CMX/45GMX/45CMX-K motherboards.

  o Pascal Terjan <pterjan@mandriva.com>
    - Fix function keys on EeePc, some NEC and some other laptops
    - Fix Wlan and Webcam keyboard switching on EeePc
    - Fix disable camera on EeePc breaking USB

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.27-rc7-git5
      * drop net-wireless-ath9k-connectivity-is-lost-after-Group-rekeying-is-done.patch
        (merged)
      * drop USB-revert-recovery-from-transient-errors.patch (merged)
      * Update security-apparmor-2.6.27.patch due to change in mm/tiny-shmem.c
      * Add usb-storage-uss725-build-fixes.patch

* Mon Sep 23 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.27-0.rc7.1.1mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Support fn key on Apple Wireless keyboards (#44119)

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Update to 2.6.27-rc7-git1
    - Disable e1000e module until a fix for its corruption issue is
      available (#44147).
    - Remove already applied fs-xfs-fix-remount-failure.patch

* Fri Sep 19 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.27-0.rc6.5.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Revert Intel ACPI IGD OpRegion support patch addition along with
      its needed patch series, we discovered a regression on a laptop
      with 855GM when using kde4 with gfx effects enabled (X hangs in
      session startup). Probably is related to the change "i915: Add
      support for MSI and interrupt mitigation." patch at first look
      after some initial debugging made by Luiz Capitulino (we are not
      sure, needs more investigation and upstream bug report that will
      be done later, but reverting all patches for now works).
    - Remove alternative patch for kernel.org bug 7694, a proper patch
      is already on mainline.
    - Add Hercules EC-900 mini-notebook to ich_laptop short cable list
      for both ata_piix and piix.
    - ALSA: Fix ALC662 DAC mixer mutes also for auto config model.
    - New/updated ethernet drivers from Jeff Garzik netdev-2.6 tree:
      * updated atl2/jme drivers;
      * enic: Cisco 10G Ethernet NIC driver;
      * qlge: New Qlogic 10Gb Ethernet Driver.
    - Include following bug fixes from linux-wireless ML:
      * ath9k: connectivity is lost after Group rekeying is done
      * b43: Fix Bluetooth coexistence SPROM coding error for Motorola
        7010 variant of BCM4306
    - Add "mute" kernel start-up parameter to disable all log messages,
      from Tiago Salem Herrmann.

  o Pascal Terjan <pterjan@mandriva.com>
    - Really disable braille console support when it is not used (#41999)
    - Enable CONFIG_CIFS_EXPERIMENTAL to support Kerberos auth (#43933)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.27-rc6-git5
    - Update .configs

* Mon Sep 15 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27-0.rc6.3.2mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Re-enable PROFILING and OPROFILE
    - Changes in build scripts
      * Don't tar .svn to remove it afterwards
      * Don't include *~ in tarball

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Re-include a workaround for a virtualbox bug (#42776) removed in
      previous release, even with Mandriva cooker/2009.0 having a newer
      VirtualBox version that has the bug fixed. Before we had this as a
      revert of both commits e587cadd8f47e202a30712e2906a65a0606d5865
      and 2f1dafe50cc4e58a239fd81bd47f87f32042a1ee, but reverting the
      later reintroduces another bug:
      http://linux.derkeiler.com/Mailing-Lists/Kernel/2008-04/msg07574.html
      Reverting the second one is needed when reverting the first one
      that is which caught the bug in VirtualBox versions prior to 2.0.2.
      The problem is that people using other distributions or older
      Mandriva releases that contains old VirtualBox versions will not
      be able to run and test Mandriva 2009.0, so we still need to apply
      a workaround. Ubuntu has a less intrusive one (not using reverts),
      so use it instead of just fully reverting the kernel commits.
    - Added fix for 2.6.27 boot issue with xfs, fs can't be mounted rw
      (http://lkml.org/lkml/2008/9/14/135), reported by Frederik Himpe.
    - Wireless bugfixes from linux-wireless ML applicable to 2.6.27:
      iwlwifi: generic init calibrations framework
      b43: Fix QoS defaults
      b43legacy: Fix failure in rate-adjustment mechanism
      b43legacy: Fix to enhance TX speed
      libertas: clear current command on card removal

* Mon Sep 15 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27-0.rc6.3.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Added fix to build warnings in rt2860 3rdparty driver.
    - Fixed and added back mach64 drm support.
    - usb-storage: fixed and added back In-System Design USS725 USB/IDE
      bridge support patches.
    - ALSA: update to v1.0.18rc3, and fix oopses from digital slaves
      addition.
    - Update to 2.6.27-rc5-git3
    - Remove revert patch to workaround VirtualBox bug (#42776),
      VirtualBox 2.0.2 now on cooker has the bug fixed.
    - Add Intel ACPI IGD OpRegion support patch from drm-next, needed to
      enable ACPI backlight control on some newer laptops with Intel
      integrated graphics. Some other patches were needed to be applied
      also because of conflicts, they do some a bit extra changes, not
      something really wanted, but possibly also fixes some stability
      issues when using intel dri. While at it also grabbed some
      minor additional bug fixes only patches from drm-next.
    - Include Intel G41 agpgart support patch posted on LKML.
    - Add patches for detection of northbridge in family 0x11 AMD
      processors from tip/x86/iommu tree.
    - Add compatibility quirk for ALI M5229 patch posted on LKML, needed
      by pata_ali libata driver to work with M5229 in some setups.

  o Pascal Terjan <pterjan@mandriva.com>
    - Set CONFIG_LEGACY_PTY_COUNT to 0. This can be changed on the command line if
      needed and saves several seconds at boot time.
    - Changes in build scripts
      * Use the to_add value even if it was already in the defconfig

* Wed Sep 10 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.27-0.rc6.1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.27-rc6
      * Drop clockevents patch series from Thomas Gleixner (already merged)

* Fri Sep 05 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.27-0.rc5.7.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Include JMicron JMC2x0 series PCIe Ethernet Linux Device Driver
      from Guo-Fu Tseng, posted on netdev.
    - Move dkms-rt2860 into kernel package.
    - Move dkms-et131x into kernel package.
    - Add aufs into Mandriva kernel, can be used as an unionfs alternative.
      The main patch and code comes from Ubuntu (see main patch file for
      details), as they already made necessary ports to account for
      apparmor patch that we also share.
    - Downgrade unionfs to version 1.4, the main unionfs patch also
      comes from Ubuntu with minor adaptations, for the same reason as
      with aufs: it has already integrated apparmor changes. We are
      downgrading because of newer problems with unionfs 2.3 + linux
      2.6.25+, we will keep it until the problems are sorted out.
      Also backported some fixes from newer unionfs versions that were
      used on dkms-unionfs package.

  o Pascal Terjan <pterjan@mandriva.com>
    - Include r8169 patches for 8102 (patches 0001 to 0006 from 
      http://userweb.kernel.org/~romieu/r8169/2.6.27-rc3/20080818/).
      Fixes networking on Acer Aspire One and MSI Wind.

  o Thomas Backlund <tmb@mandriva.org>
    - update TomoyoLinux to 1.6.4 final

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.27-rc5-git7
    - Fix boottime hang on nvidia C51 mobos (#43475) 

* Sun Aug 31 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27-0.rc5.2.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - apply_patches: fix integrity check of 3rdparty.series/series files
      regarding unlisted patch files.
    - Updated Tomoyo Linux patches to latest version from tomoyo svn
      (r1499). It contains fixed code for locking problems with apparmor
      patches applied (http://lkml.org/lkml/2008/8/30/75).
    - Use git snapshot number in package release like is done currently
      on kernel-linus package.
    - Updated to 2.6.27-rc5-git2

* Fri Aug 29 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.27-0.rc5.1mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Move EeePc patch to eeepc-laptop

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Updated to 2.6.27-rc5
    - Rediffed/updated patches for 2.6.27:
      disable-mrproper-in-devel-rpms.patch
      hwmon-coretemp-atom.patch
    - Drop wireless and gspca backport patches for 2.6.26 already
      applied on 2.6.27
    - Drop already applied/obsoleted patches:
      net-usb-rndis_host-support-WM6-devices-as-modems.patch
      acpi-compal-laptop-0.2.5.patch
      kernel-sched-disable-hrtick.patch
      3rd-3rdparty-merge.patch
      net-atl1e-driver.patch
      net-atl1e-fix-no-pm-build.patch
      pci-fix-boot-time-hang-on-g31-g33-pc.patch
    - Remove 3rdparty at76_usb driver, include the version present in
      wireless-testing tree on git.kernel.org
    - Fix tomoyo to build under 2.6.27 (vfs changes).
    - Fix ndiswrapper 1.53 to build with 2.6.27
    - Added more fixes to 3rdparty/modules for build with 2.6.27
      (prism25, unionfs, acx, ipset)
    - Removed separated apparmor patches, and include port for 2.6.27
      from Ben Collins (Ubuntu). Also fixed some still present warnings.
    - Added apparmor patch from John Johansen fixing ptrace lsm hooks,
      forwarded by Ben Collins (Ubuntu).
    - Include updated atl2 driver version.
    - Remove unused ppc arch support, unified with powerpc on 2.6.27
    - Re-import alsa 1.0.18rc1 patch, now against 2.6.27 and is a
      snapshot of alsa git repository (with changes after 1.0.18rc1).

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Fix VirtualBox boot time crash (#42776)
    - Update squashfs to v3.4

* Wed Aug 21 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26.3-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Remove unused net-wireless-bcm43xx-dont-flood-syslog-with-ifplugd.patch
      (broken), bcm43xx was removed in 2.6.26
    - Backport most of the wireless changes from 2.6.27 (until ath9k
      addition). Applied also a leds subsystem fix for a bug that
      affects the newer b43 version.

  o Pascal Terjan <pterjan@mandriva.com>
    - Add Atom support in coretemp
    - Map Acer Aspire One to acer model to get internal/external speaker, and
      external mic to work.

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Revert unionfs v2.4 update: it is buggy and One LiveCD is getting
      OOPses.

  o Thomas Backlund <tmb@mandriva.org>
    - Update Alsa to 1.0.18rc1
    - disable CONFIG_SCHED_HRTICK as it's known to cause boot problems with 
      at least Intel GMA cards, as noted on LKML and kernel BugZilla #10892
    - update to 2.6.26.3
    - revert rtl8187-fix-lockups-due-to-concurrent-access-to-config-routine
      as it's already included in the wireless backport
  
* Thu Aug 14 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26.2-2mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Add Atheros L1E Gigabit Ethernet driver from 2.6.27-rc2 (#41551)
    - Drop x86-debug-boot.patch. It is confusing a lot of people, the patch was
      supposed to help rather than causing any harm (#41946)
    - Disable PCI MSI by default, because it is known to cause boot hangs
      (patch from Fedora)

  o Pascal Terjan <pterjan@mandriva.com>
    - Obsolete dkms-iwlwifi (#42766)

* Thu Aug 07 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26.2-1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update unionfs to v2.4

  o Thomas Backlund <tmb@mandriva.org>
    - update TomoyoLinux to 1.6.3 and enable it
    - make TomoyoLinux boot-time message more userfriendly
    - fix TomoyoLinux tomoyo_network build with gcc-4.3.1
    - update to 2.6.26.2

* Sat Aug 02 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.26.1-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - sis190: fix link status on some devices.
    - Added alsa 1.0.17 fixes/updates from 2008-07-27 LKML submission.
    - Disabled CONFIG_SND_SOC on i386, there is no use for it now.
    - Integrate gspcav2 from kernel 2.6.27
    - Add synce 'dirty patch' from John Carr, fixes support for quite a
      lot of Windows Mobile devices in rndis_host, requested by
      Adam Williamson.
    - Updated to 2.6.26.1

  o Pascal Terjan <pterjan@mandriva.com>
    - Fix sound on NEC Versa S9100
    - Add upstream patch to support EeePc P900A and P901

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Drop video-bootsplash-3.1.6-2.6.25.patch, we use splashy now.

* Wed Jul 23 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.26-2mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Disable CONFIG_USB_MOUSE and CONFIG_USB_KBD: their usage is only useful
      in embedded systems and are known to cause problems in desktops.

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Disable CONFIG_FIRMWARE_EDID on i386 and x86_64 also on cooker's
      kernel, like on latest 2008.1 kernel update candidate (enhances
      boot time in some cases by a considerable amount).

  o Thomas Backlund <tmb@mandriva.org>
    - drop spec fix for #29744, #29074 (not needed anymore)
    - support WM6 devices to be used as modems
    - update drbd to 8.2.6

* Mon Jul 14 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26-1mnb
  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.26 final
    - update alsa to 1.0.17 final

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Fix typos from signal_32/64.h merge

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update apparmor to r1292 (untested)
    - Remove old apparmor from patches-broken

* Fri Jul 11 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26-0.rc9.1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Fix regression of fakerel not using anymore mkrel macro (and use
      manbo_mkrel for manbo packages).
    - create_configs: enable CONFIG_HIGHMEM4GB for desktop586 kernel
      flavour.
    - Added fs-squashfs3.3-f_pos-wrong-decrement.patch, small bug fix
      for squashfs.
    - Really don't remove bounds.h and asm-offsets.h with make clean.
    - kernel-source package shouldn't have a prepared environment, user
      is responsible to prepare and configure it for build/external use
      (don't prepare it anymore and clean uneeded files with make
      mrproper). Also, kernel*-devel packages needs a prepared
      environment, this was already assured before by the build, but
      anyway prepare the tree again to check for possible errors.
    - Backport RTL8187B support for rtl8187 from wireless-testing.
    - Disable also *config, prepare and scripts targets on kernel*-devel
      packages (previously we only disabled mrproper).

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.26-rc9
    - update Alsa to 1.0.17rc3
    - update summary and description for desktop586 kernel to reflect
      that they now support 4GB

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.26-rc9-git8

* Thu Jul 03 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26-0.rc8.1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.26-rc8-git2
    - net-netfilter-IFWLOG-mdv.patch: export ipt_IFWLOG.h to user-space, iptables
      and any IFWLOG user will need it
    - net-netfilter-psd-mdv.patch: export ipt_psd.h to user-space, iptables
      and any psd user will need it
    - Explicitly enable PARAVIRT_GUEST to fix 2.6.26-rc8 compilation

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.26-rc8
    - update ndiswrapper to 1.53
    - add missing viahss MODULE_LICENSE

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Disable smack due to more issues with unionfs.
    - Updated to 2.6.26-rc8-git3, and removed 3rdparty uvcvideo as it's
      now in upstream kernel.

* Tue Jun 24 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26-0.rc7.1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.26-rc7-git2
      * Drop acpi-video-ignore-unsupported-devices.patch (merged upstream)

* Thu Jun 19 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26-0.rc6.1mnb
  o Thomas Backlund <tmb@mandriva.org>
    - disable CONFIG_USB_RIO500, as it will switch to libusb (#41504)
    - update to 2.6.26-rc6-git3
    - drop x86-xen-time-prevent-gcc-4.3-optimizations.patch (fixed differently
      upstream, commit: f595ec964daf7f99668039d7303ddedd09a75142)  
    - update Alsa to 1.0.17rc2
    - add dvb-core header files to -devel rpms so it's possible to build 
      external dvb drivers without needing full source (#41418)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.26-rc6-git6

* Thu Jun 12 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26.rc5-1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.26-rc5-git6
      * Drop smack-fuse-mount-hang-fix.patch (merged upstream)
    - Temporary fix for Smack and unionfs deadlock
    - Boot debug patch for x86 and x86_64: with it it is possible to have
      a good idea of where the boot process has stopped
    - Fix typo in my email address used in the package's changelog
      (caught by Anssi Hannula)

  o Anssi Hannula <anssi@mandriva.org>
    - do not remove modules.* before calling depmod in %%install (fixes
      missing modules.order file)

* Tue Jun 03 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26.rc4-2mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.26-rc4-git5
      * rediff usb-ehci-hcd-isoc-sync-transfer-fix.patch
    - Update rfswitch to v1.3
    - Update atl2 network driver to v2.0.4
    - Update drbd to v8.0.12
    - Drop fs-ntfs-rw-support-as-module-option.patch, we use ntfs-3g (fuse)
      for ntfs write support
    - Fix fuse hang caused by SMACK (#40620)

  o Thomas Backlund <tmb@mandriva.org>
    - add unionfs 2.3.3 support back
    - fix unionfs umount_begin for 2.6.26 series kernels
    - drop patch input-tablet-wacom-0.8.0 as it already is in 2.6.26-rc4
    - drop usb-fix-USB-Persist-suspend, it's fixed upstream in 2.6.26-rc1
      (commit 5e6effaed6da94e727cd45f945ad2489af8570b3)
    - update prism25 to 0.2.9-r8159 and enable it
    - add patch to adapt prism25 to new netdev structure
    - fix HD-audio controllers inaccurate IRQ timing of PCM period updates.
      Needed for next version of PulseAudio (requested by Colin Guthrie)
    
* Mon May 26 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26.rc4-1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.26-rc4
      * Update disable-mrproper-in-devel-rpms.patch
    - Update create_quilt_tree: add support for -rc, -git and -stable patches
    - Fix kernel-devel: we should include the kernel/bounds.c file, otherwise
      it is not possible to run 'make prepare' on kernel-devel and dkmss
      will fail because of the missing bounds.h (which is generated by
      bounds.c)

  o Anssi Hannula <anssi@mandriva.org>
    - Obsolete kernel-laptop-devel-latest

  o Thomas Backlund <tmb@mandriva.org>
    - drop net-usb-rndis_host-wm5-6.patch, fixed differently upstream

  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Fix build with gcc 4.3 when xen guest support is enabled.

* Mon May 19 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.26.rc3-1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Enable CONFIG_USB_SUSPEND for i386 and x86_64 (#40482)
    - Enable CONFIG_HID_DEBUG for all archs (#40501)
    - 2.6.26-rc3 rebase
      * Broken patches/drivers
        * net-atl2-2.0.3.patch
        * acpi-fix-double-video-proc-entries.patch
        * net-r8169-fix-past-rtl_chip_info-array-size-for-unknown.patch
        * net-wireless-bcm43xx-dont-flood-syslog-with-ifplugd.patch
        * sound-pcsp-Don-t-build-pcspkr-when-snd-pcsp-is-enabled.patch
        * net-r8169-fix-oops-in-r8169_get_mac_version.patch
        * net-atl2-linux-2.6.24.patch
        * usb-fix-USB-Persist-suspend.patch
        * fs-fat-allow-utime.patch
        * input-tablet-wacom-0.8.0.patch
        * fs-unionfs-2.3.3_for_2.6.25.patch
        * march64 drm driver
        * prism25 wifi driver
        * rfswitch driver
      * Dropped (applied upstream)
        * sound-alsa-git-2008-04-24.patch
        * sound-pcsp-Don-t-build-pcspkr-when-snd-pcsp-is-enabled.patch
        * net-r8169-fix-past-rtl_chip_info-array-size-for-unknown.patch
        * net-r8169-fix-oops-in-r8169_get_mac_version.patch
        * fs-fat-allow-utime.patch
      * Updated
        * irq-debug-shared.patch
    - Update all .config files

* Mon May 12 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.25.3-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Fix/update broken patches for 2.6.25:  
      * fixed x86-default_poweroff_up_machines.patch
      * added updated compal-laptop patch
      * ppsci rediff/updates
      * updated mach64 drm support
      * added Phillip Lougher's patch for squashfs 3.3 on 2.6.25
      * updated wacom from linuxwacom.sf.net (0.8.0)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - 2.6.25.3
    - Drop the following patches/drivers from patches-broken
      * acer_acpi: kernel 2.6.25 provides acer_wmi, which should be used
        instead
      * kernel-sysctl_check-remove-s390-include.patch (fixed upstream)
    - Fix/update broken patches for 2.6.25:
      * fixed Intel's HECI driver
      * updated netfilter PSD
      * fixed scsi-megaraid-new-sysfs-name.patch

* Tue May 06 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.25.1-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Add max_iso_pkts parameter to uvcvideo, to limit its memory usage on
      memory constrained systems.
    - Removed sound-sigmatel_audio_fix_macbook_v2.patch (it's broken,
      does nothing, where is pin cfg assigment for model it adds?).
    - Rediffed and updated bootsplash patch for 2.6.25
    - Included following r8169 fixes from Linus tree:
      "r8169: fix past rtl_chip_info array size for unknown chipsets"
      "r8169: fix oops in r8169_get_mac_version"
      They were tested by Adam Pigg and fixed an oops with his machine.

  o Pascal Terjan <pterjan@mandriva.com>
    - Rediffed acpi-asus-eee.patch
    - Obsolete kernel-laptop-latest in kernel-desktop-latest

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - 2.6.25.1
    - Update package's URL

* Tue Apr 29 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.25-1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - 2.6.25 rebase
      * Update acpi-dsdt-initrd-v0.8.4-2.6.21.patch (for 2.6.25)
      * Update unionfs to v2.3.2 (for 2.6.25-rc7)
      * Broken drivers
        * drbd-8.0.11
        * squashfs
        * HECI
        * Acer ACPI
        * USB uss725 storage
        * Unicom
        * Apparmor
        * Bootsplash
        * ppscsi
        * Netfilter PSD
        * BadRam
        * Wacom Tablet 0.7.9-8
      * Dropped patches (already merged upstream)
        * usb-atm-cxacru-zte-zxdsl-id.patch
        * acpi-add-aliases-to-toshiba_acpi-module.patch
        * hid-usbhid-blacklist.patch
        * hwmon-applesmc-macbook2.patch
        * char-agp-add-support-for-662-671-to-agp-driver.patch
        * char-i8k-inspiron-e1705-fix.patch
        * char-agp-sis-Suspend-support-for-SiS-AGP.patch
        * char-drm-add-new-rv380-pciid.patch
        * char-i8k-adds-i8k-driver-to-the-x86_64-kconfig.patch
        * char-i8k-allow-i8k-driver-to-be-built-on-x86_64-systems.patch
        * char-i915-Add-chipset-id-for-Intel-Integrated-Graphics-D.patch
        * char-intel-agp-add-new-chipset-ID.patch
        * capabilities-remove-cap-task-kill.patch
        * char-nozomi-driver.patch
        * net-igb.patch
        * net-wireless-rt2500usb-add-id.patch
        * x86-cpufreq-add-missing-printk-levels-to-e_powersaver.patch
        * x86-cpufreq-e_powersaver-add-c7d-support.patch
        * x86-cpufreq-powernow-k8-update-to-support-latest-turion.patch
      * Fix prism25 Kconfig. Keyword 'enable' doesn't exist in 2.6.25
      * Update .configs and create_configs script
      * Enable CONFIG_LATENCYTOP
    - Enable CONFIG_SMACK for i386 and x86_64
    - Drop -laptop package: as it has been discussed, we are almost sure
      that the -laptop package does not save much power if compared to
      -desktop package with CONFIG_NO_HZ enabled.
    - Minor spec cleanups
       * Break comments in 80 columns
       * Fix typos in comments
       * Use variables for some duplicated paths
    - Change update_configs to exit on failure, useful to catch broken
      Kconfigs
    - Introduce kcooker-rebase script: helper for the rebase work
    - Drop all patches-broken contents from previous 2.6.24 rebase

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Removed 3rd-uvc-limit-max-iso-packets.patch, I found one type of
      webcam that doesn't like it, so just revert.
    - Updated unionfs to version 2.3.3
    - Updated uvcvideo to r205, and removed already applied
      3rd-uvc-x300.patch
    - Updated alsa to latest LKML submission (git-2008-04-24), and
      removed patches already applied upstream.
    - Add patch from Linus tree: "pcsp - Don't build pcspkr when
      snd-pcsp is enabled". It seems we don't have the full set of
      2.6.26 alsa submission... needed to avoid building pcspkr and
      snd_pcsp as they conflict.

  o Pascal Terjan <pterjan@mandriva.com>
    - Dropped media-usbvideo-device-link.patch, merged upstream

* Mon Mar 30 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.4-2mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - iwlwifi: Initialize rf_kill status
    - asus_acpi: Fix brightness handling on EeePc
    - Alsa (snd-hda-intel) : Set correct model for TOSHIBA Satellite Pro A200
      and A210
    - drop ipt_time patch, xt_time was now included
    - fix a crash in uvcvideo on X300 (upstream r199)

  o Olivier Blin <oblin@mandriva.com>
    - make kernel-<flavour>-devel-latest provide kernel-devel-latest (#36524)

* Thu Mar 27 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.4-1mnb
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Alsa (snd-hda-intel) bug fixes/additions/cleanups:
      * Added support model for Clevo M720R from upstream alsa
        (by Jiang zhe).
      * Cleanups after DAC assignment order in ALC883.
      * Support mic automute in Clevo M720R, and map Clevo M720SR to use
        the same model (they are identical). Also choose a more generic
        model name ("clevo-m720").
      * Add optimized ALC267 model for Quanta IL1.
    - Fix spec License tag as per current license policy (GPL -> GPLv2),
      reported by Gustavo De Nardin (spuk).
    - ACPI: limit Clevo M720SR to C2 processor idle state (machine
      freezes with C3).

  o Pascal Terjan <pterjan@mandriva.com>
   - Alsa (snd-hda-intel) : Set correct model for Sony Vaio VGN FZ18M
   - Rewrite patch for Asus ACPI keys (still #23741).
   - Don't break ACPI support when the child of a video bus device is not a
     video device (kernel bug #9761)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
   - Disable MSI on i386. MSI seems to be still problematic and some
     machines are not booting because of it, so it's better to stay safe
     for now and just disable it again
   - Update to 2.6.24.4
     * rediff capabilities-remove-cap-task-kill.patch
   - Update unionfs to 2.3.1
     * dropped fs-unionfs-2.2-apparmor-2.1.patch and addded a rediffed
       version named fs-unionfs-2.3-apparmor-2.1.patch

* Thu Mar 20 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.3-4mnb
  o Pascal Terjan <pterjan@mandriva.com>
    - Generate input events for ACPI hotkeys in asus-laptop and autoload it
      instead of asus_acpi (#23741).

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Include bttv.h and bttvp.h headers in kernel-devel, required by
      dkms-lirc-gpio (#39004, patch by Anssi Hannula <anssi@mandriva.org>).
    - Alsa (snd-hda-intel) bug fixes:
      * Fix DAC assignment order in ALC883.
      * Choose correct ALC883 codec model for MSI 945GCM5 V2 (MSI-7267).

  o Shinji Makino <shinji@turbolinux.co.jp>
    - added video-char-union-bootsplash-unicon.patch (#37928).

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Fix apparmor OOPS because of FUSE accessing ia_file
      unconditionally (#38688)

* Fri Mar 14 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.3-3mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Add back cpufreq tables for Centrino Dothan in speedstep-centrino
      (#38760)
    - Update fs-fat-allow-utime.patch with a new default initialization,
      which allows all users to use utime() on files if the directory
      is writable

  o Pascal Terjan <pterjan@mandriva.com>
    - Fix asus_acpi patch, latest commit broke keys handling

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Alsa (snd-hda-intel) bug fixes:
      * Fixed mute switches of ALC662 mixers (generic models).
      * Choose correct ALC662 codec model for Asus P5GC-MX.

  o Thomas Backlund <tmb@mandriva.org>
    - Fix kernel-source symlinks if the kernel is installed after the
      source and no matching -devel- rpm is installed (#38862)
    - add support for WM5/6 devices (#30128)

* Mon Mar 10 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.3-2mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Drop tomoyo linux patches from patches-purgatory/, they have been
      merged already
    - Introduce svn-tag-kernel script
    - Add BadRAM
    - Disable BadRAM on x86_64, it doesn't compile if CONFIG_DISCONTIGMEM
      is enabled
    - bluetooth: fix OOPS in l2cap_conn_del()
    - bluetooth: fix eSCO connection (#37272)
    - fat: allow utime() (#26819)

  o Pascal Terjan <pterjan@mandriva.com>
    - Suggest restarting the system after installing a new kernel
    - Fix sound on NEC S970
    - Update the asus_acpi patch for EeePc :
      * Have the mute and volume keys generate input events
      * Use the [AP] (fn+f6) key to enable/disable the webcam
      * Don't handle wireless switching, we didn't do anything anyway
    - Add a new id for rt2500usb (#38512)
    - Add a device link in /sys/class/video4linux/video*/ else hal don't see
      them (and device does not get the needed acl) 

  o Shinji Makino <shinji@turbolinux.co.jp>
    - added usb-storage-unusual_devs-add-id.patch 

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Added some x86 cpufreq updates from Linux 2.6.25-rcX:
      * CPUFREQ: Powernow-k8: Update to support the latest Turion
        processors;
      * CPUFREQ: Support Model D parts and newer in e_powersaver;
      * CPUFREQ: Add missing printk levels to e_powersaver.
    - Added patch to e_powersaver to limit processor voltage/multiplier
      status printed to syslog (avoid flood of messages when we have
      ondemand governor and many P-state changes for example).
    - Backport/add intel igd, sis 662/671, ati rv380 drm/agp support and
      sis-agp suspend support from 2.6.25-rcX.

* Mon Mar  3 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.3-0.1mnb
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Drop the following patches: block-scsi_ioctl-GPCMD_SEND_KEY.patch,
      input-export-module_device_tables.patch and
      char-export-module_device_tables.patch from patches-purgatory/.
      According to Shinji Makino this Turbo Linux patch is not needed anymore
    - Remove cap_task_kill() to fix kill() semantic bug (#37328)
    - Enable CONFIG_PCI_MSI on i386: MSI had to be disable in 2.6.22 because
      of a bug which caused PCI to stop working on some machines. It seems
      it's safe to enable again now.

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Drop char-intel-agp-revert-revert-fix-stolen-mem-range-on-G33.patch
      x11-driver-video-intel reverted the change that required this, as
      reported by Colin Guthrie.
    - Added fix from alsa hg tree (5846):
      "hda-codec - Don't create vmaster if no slaves found"
      This should address problems with mixers without any slave control
      defined for models in codecs with vmaster control being used, and
      will fix mandriva bug #37984
    - hda-intel - Fix Oops with ATI HDMI devices, fix from alsa hg
      change 5873
    - Added patch from Alan Stern to fix reported USB-Persist+suspend
      issues (one of the problems found while testing on Intel
      Classmate).
    - Updated to 2.6.24.3
    - Disable control group support and fair group cpu scheduler for
      default configs.
    - scripts/create_configs:
      * enable cgroup/fair group scheduler options for server kernel
        flavour;
      * remove SWAP_PREFETCH and ADAPTIVE_READAHEAD config option uses
        (we don't have them anymore).
    - Added patch from Andrey Borzenkov that add aliases to toshiba_acpi.
      With this module autoloading is possible for devices which aliases
      are added (suggested by Olivier Blin).

  o Pascal "Pixel" Rigaux <pixel@mandriva.com>
    - use %manbo_mkrel for Manbo Core 1
    - rename %mdvrel into %mnbrel
    - get rid of %mkrel usage (using plain release with no distsuffix)
    - replace (old) versioned buildrequires with plain buildrequires
    - %ktag is now mnb
    
  o Shinji Makino <shinji@turbolinux.co.jp>
    - added tomoyolinux-build.patch, tomoyolinux-support.patch and 
      tomoyolinux-apparmor-union.patch
    - change to kernel configuration.
      added to i386.config,x86_64.config was enable tomoyolinux.
      added to powerpc.config,ppc.config,sparc64.config was disable tomoyolinux.

  o Pascal Terjan <pterjan@mandriva.com>
    - added NF_MATCH_TIME support
    - use rpmbuild instead of rpm in our Makefile

  o Thomas Backlund <tmb@mandriva.org>
    - enable PANTHERLORD_FF and ZEROPLUS_FF (#38213)
    - update ndiswrapper to 1.52
    - add Prism2 support back (#38155)
    - update acer_acpi to 0.11.1
    - update wacom tablet to 0.7.9-8 (#37073)
      * bugfixes, adds support for Wacom Cintiq 20WSX
    - add usb hid quirk for Multilaser USB-PS/2 keyboard adapter (#36870)
    - add fixes and addons from Alsa HG tree:
      * hda-codec fix ALC880 F1734 model
      * hda-codec fix automute of AD1981HD hp model
      * hda-codec fix wrong capture source selection for ALC883 codec
      * hda-codec fix ALC882 capture source selection
      * hda-codec clean up capture source selection of Realtek codecs
      * hda-codec implement auto mic jack-sensing for Samsung laptops with AD1986A
      * hda-codec more auto configuration fixups
      * hda-codec fix auto configuration of realtek codecs
      * hda-codec add IEC958 default PCM switch
      * hda-codec add more names to vendor list
      * hda-codec fix breakage of resume in auto-config of realtek codecs
      * hda-intel add ATI RV7xx HDMI audio support
      * hda-codec fix amp-in values for pin widgets
      * hda-codec fix missing capsrc_nids for ALC262
      * hda-codec add support for AD1883, AD1884A, AD198A, q984B
      * hda-codec add model=mobile for AD1884A
      * intel8x0 add support for 8 channel sound
      * hda-codec fix master volume on HP dv8000
      * bt87X fix freeing of shared interrupt
      * hda-codec fix ALC662 recording
      * hda-codec fix ALC268 capture source
      * hda-codec fix STAC927x power management
      * hda-codec fix STAC927x invalid association value
      * hda add PCI_QUIRKS for laptops with 92HDxxxx codecs
      * hda STAC927x support analog mic
      * seq_oss_synth remove invalid bug()
      * hda-codec add missing descriptions for STAC codec models
      * hda-codec adapt eeepc p701 mixer for virtual master control
      * usb-audio add workaround for broken E-Mu frequency feedback
      * usb-audio sort quirks list
      * sb8 fix sb 1,0 capture DMA programming
      * hda-codec fix AD1988 capture elements
      * hda-codec add Fujitsu Lifebook E8410 to quirk table
      * hda-codec fix initial DAC numbers of 92HD71bxx codecs
      * oxygen add owner field
      * hda-codec add docking station mic input for Thinkpad X61
      * hda-codec fix names of realtek codecs to adapt master controls
      * intel8x0 add quirk for Compaq Deskpro EN
      * hda-sigmatel disable power management on fixed ports
      * hda-sigmatel add verbs for 92hd73xxx laptops
      * hda-codec fix array over-range access with stac92hd71bxx codec

* Thu Feb 21 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.2-4mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Drop pci-pciaddress-64bit-fix.patch from patches-purgatory/. According to
      Shinji Makino this Turbo Linux patch is not needed anymore
    - Update unionfs to 2.2.4
    - Introduce HECI v3.2.0.24 driver (to support Intel's AMT)

  o Shinji Makino <shinji@turbolinux.co.jp>
    - fix diff flie video-char-enable-unicon.patch
    - delete patches x86-apm-smp-power_off.patch
    - add patches x86-default_poweroff_up_machines.patch

  o Thomas Backlund <tmb@mandriva.org>
    - add compal-laptop driver (#37860)
    - disable CONFIG_USB_OHCI_HCD_SSB so ssb wont get loaded even if it
      is blacklisted (reported by AdamW on kernel-discuss)
    - update Wacom tablet support (#37073)
      * adds support for: Bamboo1, BambooFun and Cintiq 12WX
    
* Mon Feb 18 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.2-3mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Special release due to compilation problems in the previous one

* Fri Feb 15 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.2-2mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - scripts/create_quilt_tree: add a hack to support mainline patches
    - scripts/create_quilt_tree: report errors when creating the tree
    - Fix apparmor boottime flag handling
    - Actually move patches into patches-purgatory directory. The following
      patches: block-cciss-ioctlret.patch, block-scsi_ioctl-GPCMD_SEND_KEY.patch,
      pci-pciaddress-64bit-fix.patch, usb-storage-unusual_devs.patch,
      char-export-module_device_tables.patch, input-export-module_device_tables.patch
      were deleted instead of being moved into the purgatory dir. Add them back in
      the expected location
    - Update drbd to v8.0.11
    - Drop input-alps-pad-fix.patch according to Shinji Makino this TL
      patch is not needed anymore

* Mon Feb 11 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24.2-1mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Introduces PATCHES/Documentation directory
    - Introduces kernel-build-svn-checkout.txt, managing-patches.txt,
      patch-format.txt, README documents
    - Introduces create_quilt_tree script
    - Move tomoyo patches into patches-purgatory

 o Thomas Backlund <tmb@mandriva.org>
    - update alsa to 1.0.16 final
    - add selected fixes from alsa HG tree:
      * sound-soc-fix-duplicate-rj-master-test.patch
      * sound-hda-intel-Fix-PCM-device-number-assignment.patch
      * sound-hda-codec-Add-ID-for-HDMI-codec-on-Jetway-J9F2.patch
      * sound-ice1712-Fix-hoontech-MIDI-input.patch
      * sound-hda-STAC927x-power-down-inactive-DACs.patch
      * sound-hda-intel-use-SG-buffers.patch
      * sound-hda-intel-support-64bit-buffer-allocation.patch
      * sound-ice1712-add-support-for-Delta1010E.patch
      * sound-ice1712-all-support-for-Delta-66E.patch
      * sound-hda-intel-Fix-compile-error-with-CONFIG_SND_DEBUG_DETECT.patch
      * sound-hda-codec-correct-HDMI-transmitter-names.patch
      * sound-hda-codec-remove-duplicate-controls-in-alc268-test-mixer.patch
    - disable inclusion of s390 file in sysctl_check as we dont ship arch/s390 
      files in our kernel-source (#37388)
    - update to 2.6.24.2 
      * CVE-2008-0007, CVE-2008-0009/10, CVE-2008-0600
    - drop mm-zerolen-iov-fix.patch (merged upstream)
    
 o Pascal Terjan <pterjan@mandriva.com>
    - Add patch by Nick Piggin fixing pan going unkillable (#37050)

 o Shinji Makino <shinji@turbolinux.co.jp>
    - Initial Turbo Linux patch merge

 o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Added updated AppArmor patches for 2.6.24 (thanks to John Johansen
      at Suse for them).

* Tue Jan 29 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-1mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.24
    - Dropped kernel-sched-cpu_share-tunable-crash-fix.patch (already in 2.6.24)
    - Dropped net-sis190-sis968.patch (already in 2.6.24)
    - Update unionfs to 2.2.2
    - Remove badram patch from patches-broken (there's no up to date version
      for 2.6.24, we can add it later if needed)
    - Enable all CONFIG_TASKSTATS options for i386 and x86_64
    - Enable TIPC network protocol for i386
    - Enable PREEMPT_BKL for -desktop kernels (i386 and x86_64)
    - Fix unionfs OOPS when umounting root partition when there's a nfs volume
      in the branch

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated nozomi driver patch with version added recently to Linus
      tree (pre 2.6.25, commit 20fd1e3bea554620d489f3542496639c1babe0b3,
      char-nozomi-driver.patch).
    - Updated uvcvideo to svn r173 (and removed already applied
      3rd-uvc-stream-no-fid.patch).

* Wed Jan 23 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-0.rc8.2mdv2008.1
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Added fix for isochronous transfer bug in ehci-hcd, adding patch
      from http://bugzilla.kernel.org/show_bug.cgi?id=7694
      I experienced the same issue but when using uvcvideo with a Syntek
      webcam (174f:5212), after some time the streaming fails with
      -EL2NSYNC. The patch there fixed the problem.
  - Updated uvcvideo to r166.
  - Replaced previously added sync quirk for Syntek webcam with a better
    version, that avoids losing sync of frames by using reported EOF
    marker. For more details see:
    https://lists.berlios.de/pipermail/linux-uvc-devel/2008-January/002779.html
    (final patch by Laurent Pinchart)

  o Pascal Terjan <pterjan@mandriva.com>
    - Added Intel(R) 82575 Gigabit Ethernet driver (igb)

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.24-rc8-git5
    - update alsa to 1.0.16rc1
    - drop sound-Fix-5.1-sound-in-Dell-6stack-ALC888-HDA.patch (merged upstream)
    - add sched cpu_share tunable crash fix (Mingo, LKML)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Fix ipt_IFWLOG user-space header (#37082)
    - Fix apparmor disable flag (apparmor doesn't work yet though #36004)

* Thu Jan 17 2008 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-0.rc8.1mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.24-rc8-git1

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Modified kernel configs:
      * i386.config: enabled USB_EHCI_ROOT_HUB_TT (y) and
                     USB_ISP116X_HCD (m).
      * x86_64.config: likewise, and also enabled
                       CONFIG_USB_SL811_HCD (m) and
                       CONFIG_USB_SL811_CS (m).

 o Thomas Backlund <tmb@mandriva.org>
    - make 32bit kernels conflict arch(x86_64) so they cant be installed
      by mistake (#32631)

* Mon Jan 14 2008 Herton Ronaldo Krzesinski <herton@mandriva.com> 2.6.24-0.rc7.2mdv2008.1
  o Thomas Backlund <tmb@mandriva.org>
    - add support for Dell i8k on x86_64 (#32447)
    - disable XEN Guest support on all but server kernels as it breaks 
      AGP support (#36458)

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - 3rdparty addition: AuthenTec AES2501 Fingerprint Sensor Driver for
      Linux. Added in tree build support and oops on module removal fix
      when device isn't available:
      3rd-aes2501-kbuild.patch
      3rd-aes2501-rmmod-oops-fix.patch
    - Added patch from Claudio S. Matsuoka that fix 5.1 sound in Dell
      6stack ALC888 HDA, currently used in Dell Inspiron 530
      (sound-Fix-5.1-sound-in-Dell-6stack-ALC888-HDA.patch)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.24-rc7-git5

* Mon Jan 07 2008 Herton Ronaldo Krzesinski <herton@mandriva.com> 2.6.24-0.rc7.1mdv2008.1
  o Thomas Backlund <tmb@mandriva.org>
    - change url to Mandriva wiki
    - fix build,source symlinks to -source tree to be created only if no
      matching -devel tree is installed, and to be removed only if they
      point at the -source tree
    - move defcofigs to the correct location for i386 and x86_64, prefix 
      them the same way as upstream, and drop defconfig-maximum
    - use make clean on -devel & source tree to not ship unneeded files
    - more spec cleanups
    - update to 2.6.24-rc7

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated alsa to latest hg/git tree, mostly because of bug fixes
      and hda-intel updates, so we can test it early. Reverted some
      commits though so we can still use userspace lib/utils from alsa
      1.0.15, if some revert is missing it's a bug.
    - Enabled SND_HDA_POWER_SAVE (Aggressive power-saving feature of
      snd-hda-intel), and keep the default Kconfig choice of automatic
      power-save mode (disabled = 0).

* Fri Jan 04 2008 Herton Ronaldo Krzesinski <herton@mandriva.com> 2.6.24-0.rc6-3mdv2008.1
  o Pascal Terjan <pterjan@mandriva.com>
    - Add mactel patches (#35420)
    - Add support for EeePc in asus_acpi

  o Thomas Backlund <tmb@mandriva.org>
    - update unionfs to 2.2
    - update source2 to apply cleanly
    - update alsa krpovides

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated to 2.6.24-rc6-git10, rediffed irq-debug-shared.patch
    - Update unionfs again, now to version 2.2.1
    - Added back apparmor for 2.6.24 from Suse (with minor patch changes
      in hunks that touch reiserfs code, as it didn't apply by default
      because our reiserfs differs. Also needed to fix build when
      cgroups is enabled).
    - Brought back and redid patch to fix build of unionfs with
      apparmor.

* Fri Dec 28 2007 Herton Ronaldo Krzesinski <herton@mandriva.com> 2.6.24-0.rc6-2mdv2008.1
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated uvcvideo to svn r158
    - Add new sync quirk to uvcvideo and use it (needed by Syntek
      174f:5212 webcam), from Claudio S. Matsuoka <cmatsuoka@gmail.com>
    - Prevent uvcvideo to alloc too much memory in usb_buffer_alloc,
      lowering UVC_MAX_ISO_PACKETS. In machines with not much memory +
      webcam that uses isoc transfers, several calls to it can cause
      memory fragmentation or requesting too much memory resulting in an
      Page Allocation Failure (OOM). UVC_MAX_ISO_PACKETS is arbitrary, see
      http://article.gmane.org/gmane.linux.drivers.uvc.devel/1956
    - Updated to 2.6.24-rc6-git5
    - Build genrtc as module now that Mandriva's udev is now creating
      automatically the /dev/rtc symlink pointing to /dev/rtc0, making
      possible using /dev/rtc from one of the modules from new modular
      rtc framework (Reported/pointed by Dick Gevers and Andrey
      Borzenkov on cooker ML).

* Tue Dec 25 2007 Herton Ronaldo Krzesinski <herton@mandriva.com> 2.6.24-0.rc6-1mdv2008.1
  o Pascal Terjan <pterjan@mandriva.com>
    - Switch atl2 to 2.0.3, which is the branch aiming at upstream merge

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.24-rc6-git2
    - add support for upstream -git tarballs
    - update ndiswrapper to 1.51
    - update drbd to 8.0.8
    - update acer_acpi to 0.10
    - prefix 3rdparty tarballs with 3rd- to match the new patch naming scheme
    - update defconfigs
    
* Wed Dec 12 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-0.rc5-2mdv2008.1
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Removed already applied upstream alsa quirk for Dell XPS M1330.
    - scripts/apply_patches: usage message fixes.

* Wed Dec 12 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-0.rc5-1mdv2008.1
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated uvcvideo to r149, and removed already applied 
      3rd-uvcvideo-add-quirk-ali-5606.patch

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Upgrade to 2.6.24-rc5-git2
    - V4L: fix videobuf_read_start() breakage
    - Upgrade unionfs to 2.1.11

* Mon Dec 05 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-0.rc4-2mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.24-rc4-git2 (#35822)
    - Kill patches-to-drop directory: that directory exists for a long time
      and its patches seems to not be useful
    - New patch naming scheme: now patches have the following format:
      subsystem-description.patch. A detailed documentation will be provided
      shortly.
    - Better names for netfilter patches
    - Reorganize series file

  o Pascal Terjan <pterjan@mandriva.com>
    - Fix TI PCIxx12 card readers (#35887)

* Mon Dec 04 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-0.rc4-1mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.24-rc4
    - Update acpi_fix_double_video_proc_entries.patch to latest kernel
    - Merge ipt_psd patches into netfilter-psd-mdv.patch
    - Merge ipt_IFWLOG patches into netfilter-IFWLOG-mdv.patch
    - Update ipt_IFWLOG to v1.1

* Tue Nov 27 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-0.rc3-2mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.24-rc3-git1

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Added quirk for uvcvideo, needed by the webcam found on Clevo
      M540SR (ALi 5606).
    - Enabled XEN guest, suggested by Olivier Blin
      (http://archives.mandrivalinux.com/kernel-discuss/2007-11/msg00033.php).
    - Updated ndiswrapper to version 1.50rc3.
    - More netfilter api fixes for ipt_set and ipt_psd for 2.6.23 and
      later:
      ipset-switch-match-checkentry-to-bool.patch
      ipset-2.6.24-apifix.patch
      netfilter_psd_switch-ipt_psd_match-to-bool.patch
    - Fix return type of write file_operations callback functions in
      tc1100-wmi.

  o Thomas Backlund <tmb@mandriva.org>
    - fix -devel rpm breakage due to i386/x86_64 merge into x86
    - add /drivers/lguest/lg.h to -devel rpms

  o Pascal Terjan <pterjan@mandriva.com>
    - Blacklist in usbmouse/usbkbd devices set to IGNORE in hid quirks
      (fixes Wacom)

* Thu Nov 22 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.24-0.rc3-1mdv2008.1
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - Update to 2.6.24-rc3
    - Fix ipt_psd netfilter API usage
    - Kill PATCHES/doc directory
    - Move AppArmor patches to patches-broken directory, the -rc updates
      broke it

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Enabled CONFIG_DEBUG_BUGVERBOSE option on configs where it was
      disabled, it's useful despite some more ram usage, see
      http://archives.mandrivalinux.com/kernel-discuss/2007-11/msg00006.php
      (Suggested by Olivier Blin).
    - Updated to 2.6.24-rc2-git3.
    - scripts/create_configs: updates for i386/x86_64 arch unification;
      kernel-2.6.spec: likewise.
    - package Makefile: deal with kpatch field inside spec, to create
      the patches tarball with the correct name when it's used.
    - Updated acer_acpi to 0.10_rc4, and added needed build
      fixes/updates for 2.6.24-rc2:
      acer-acpi-extra-cflags.patch
      acer-acpi-match-dmi_system_id-callback.patch
    - Removed ipw3945, now use the iwl3945 in upstream kernel, if
      required in the case iwl doesn't work well for some devices we
      can readd it.
    - Updated squashfs to version 3.3, dropped already applied/obsolete
      squashfs-add-missing-include, squashfs-inode-fix,
      squashfs-2.6.23-buildfix patches.
    - Updated 3rdparty_merge patch for 2.6.24-rc2.
    - Updated unionfs to version 2.1.9, builds with new kernel and
      also has a fix for a self deadlock issue reported here:
      http://www.fsl.cs.sunysb.edu/pipermail/unionfs/2007-October/005536.html
    - Drop BadRAM patch until we fix it or a new version for 2.6.24 is
      available.
    - Made needed fixes for misc build/code issues required now on
      2.6.24-rc2 for extra patches/3rdparty additions:
      * ndiswrapper: ndiswrapper-proc_net-namespace.patch
                     ndiswrapper-new-napi-polling.patch
                     ndiswrapper-remove-set_module_owner.patch
                     ndiswrapper-extra-cflags.patch
      * acx: acx-remove-set_module_owner.patch
      * acerhk: acerhk-extra-cflags.patch
      * drbd: drbd-8.0.6-linux-2.6.24-fixes.patch
      * ppscsi: ppscsi-sg-helper-update.patch
      * netfilter_IFWLOG: netfilter_IFWLOG_2.6.24.patch
      * uss725: uss725-sg-helper-update.patch
                uss725-avoid-ide-fix-driveid.patch
        the uss725-sg-helper-update.patch makes
        uss725_revert_sg-address_removal.patch unecessary, so it was
        removed
      * atl2: atl2-linux-2.6.24.patch
    - Updated mach64 drm support for 2.6.24-rc2.
    - Updated uvc to r141 svn snapshot.
    - Updated apparmor patches to build again with 2.6.24-rc2, but I'm
      not sure if it still works, need more testing and probably more
      changes. I had to revert too some upstream changes that make LSM a
      static interface, it would be good to check the changes more in
      detail and migrate more apparmor bits, seems it can't be a module
      anymore.
    - Dropped ralink legacy drivers, keep now only the mac80211 ones
      integrated in linus kernel, if in the future we see we still need
      them we can readd.
    - Drop already applied patches:
      zd1211rw-more-ids
      ALSA-hda-codec-Fix-input_mux-numbers-for-vaio-st
      alsa-hg5424
      ipg
      i386-add-support-for-picopower-irq-router
      alsa-hg5408
      alsa-git-20070912
      alsa-hg5432
      alsa-hg5436
      alsa-fix-sound-oops-dell-xps-m1210
      ALSA-hda-codec-Fix-for-Fujitsu-Lifebook-C1410
      ueagle-atm-patches-eagle-iv-support
      alsa-hg5416
    - Rediffed patches:
      Toshiba_Equium_A60-needs-pci-assign-busses
      boot-video-80x25-if-break.patch
      130-netfilter-ipset.patch
      netfilter_IFWLOG.patch
      netfilter_psd.patch

* Wed Oct 31 2007 Herton Ronaldo Krzesinski <herton@mandriva.com> 2.6.23.1-1mdv2008.1
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Parallelize xargs invocations for smp machines on rpm build.
    - apply_patches:
      * remove trailings spaces, fix tabs vs. spaces;
      * introduce a different scheme to process patches: really use
        series file now, taking the patches in their order. With this we
        can drop the confusing prefixes that anyone knows for sure their
        meaning in all cases. Also use 3rdparty.series file to add third
        party additions, in the same way as series, this way we can
        document/comment third party additions inside it. It's separated
        from series file so we can use quilt for the patches;
      * fix usage output;
      * make sure no patches are forgotten in patches directory, if a
        patch or 3rdparty addition isn't listed in
        3rdparty.series/series exit with error;
      * remove reference for Juan Quintela's now invalid email address
        (reported by Thierry Vignaud).
    - Updated to version 2.6.23.1.
    - Added updated BadRam patch for 2.6.23.
    - Updated ndiswrapper to version 1.49.
    - Updated unionfs to 2.1.7; redid fix-unionfs-build-with-AppArmor
      patch because of it, and removed already applied
      unionfs-2.1.3-do-not-update-mtime-if-no-upper-branch patch.
    - Added updated version of nozomi patch from gregkh git repository.
    - Updated tc1100-wmi module patch for 2.6.23, and made fix for acpi
      subsystem updates (tc1100-wmi-2.6.23-fixes patch). Also removed
      uneeded tc1100-wmi-depends-ACPI_INTERPRETER patch.
    - Updated mach64 drm module for 2.6.23.
    - Added updated apparmor patches that apply on 2.6.23 from
      kernel-tmb.
    - Redid patches:
      pnpbios-off-as-default
      acpi_fix_double_video_proc_entries
      sis190-sis968
      boot-video-80x25-if-break
    - Added squashfs fix for 2.6.23 from kernel-tmb.
    - Added Revert-Revert-intel_agp-fix-stolen-mem-range-on-G patch, we
      don't need the upstream revert commit because our
      x11-driver-video-intel already has a patch for that change on
      kernel.
    - Added ipset 2.6.23 fixes from kernel-tmb (ipset-2.6.23-buildfix,
      ipset_2.6.23-buildfix2 patches).
    - Fix atl2 module building on 2.6.23 (atl2-linux-2.6.23 patch).
    - Drop already applied changes from ueagle-atm-patches-eagle-iv-support
      patch (and the diff is now from upstream linus git tree).
    - create_configs: update for NOHIGHMEM case, probably there is a bug
      in Kconfig selection now that asks for X86_PAE.
    - Remove already applied patches:
      USB-option-Add-a-new-device-ID-for-the-HUAWEI-E220
      PCI-Run-k8t_sound_hostbridge-quirk-only-when-needed
      sata_mv-PCI-IDs-for-Hightpoint-RocketRaid-1740-1742
      pata_marvell-Add-more-identifiers
      add-eeprom_93cx6-support
      b44-updates
      r8169_link_down_fix
      pci-fix-unterminated-pci_device_id-lists
      alsa-git-2007-07-20
      PCI-unhide-SMBus-on-Compaq-Deskpro-EP-401963-001-mo
      ipw2100-updates
      ext34_orphan_list_corruption_fix
      ipaq_htc_smartphones_support
      ACPI-dock-use-dynamically-allocated-platform-devic
      i386-do-not-restore-reserved-memory-after-hibernati
      drm-via-Fix-dmablit-when-blit-queue-is-full
      jmicron-PIO-fixes
      smbus_sb800_support
      fix_ENE_CB712-4_card_readers
      libata-clean-up-horkage-handling
      ACPI-dock-cleanup-the-uid-patch
      ata_piix-fix-pio-mwdma-programming
      myri10ge-Add-support-for-PCI-device-id-9
      usb-misc-sisusbvga-add-product-ID-of-TARGUS-MCT-dev
      hid_fix_autocentering_of_pid_devices
      unusual-devs-updates
      intel-agp-Fix-i830-mask-variable-that-changed-with
      acpi-battery-updates
      acpi-ec-updates
      USB-option-Add-Dell-HSDPA-5520-to-driver
      intel-agp-945_965_GME-G33-fixes
      mac80211-updates
      zd1211rw-updates
      ipw2200-updates
      ext34_orphan_list_check
      agp-Add-device-id-for-P4M900-to-via-agp-module
      rtl8187
      smbus_sb700_support
      libata-ahci-add-ATI-SB800-PCI-IDs
      USB-cdc-acm-add-new-device-id-to-option-driver
      pata_it821x-fix-lost-interrupt-with-atapi-devices
      pata_cs5520-Fix-probe-bug-regression-introduced-in
      add-wacom-bamboo-tablet-support
      libertas-updates
      PCI-pci_ids-add-atheros-and-3com_2-vendors
      debugfs_rename
      ata_piix-IDE-mode-SATA-patch-for-Intel-Tolapai
      USB-visor-add-ACER-S10-palm-device-id
      USB-ftdi_sio-add-of-a-new-product-manufacturer-TM
      USB-fix-support-for-Dell-Wireless-Broadband-aka-WW
      Fix-broken-pata_via-cable-detection
      libata_broken_hpa_horkage
      eeprom-93cx6-misc-fixes
      PCMCIA-NETDEV-add-new-ID-of-lan-modem-multifunctio
      pata_sis-fix-MWDMA-for-UDMA66-chipsets-and-UDMA
      forcedeth-mac-address-correct
      cdc-subset-to-support-new-vendor-product-ID
      libata-IDE-add-new-VIA-bridge-to-VIA-PATA-drivers
      airo-updates
      forcedeth-mcp73-support
      Add-the-Osprey-440-to-the-Bt878-ALSA-whitelist
      pata-hpt-clock-fixes
      Fix-sata_via-write-errors-on-PATA-drive-connected-to
      genetlink-dynamic-multicast-groups
    - Removed hrtimer patches, already applied or not relevant anymore.
    - Removed custom kvm, use the one from 2.6.23.
    - Remove swap prefetch patches, as they don't apply and aren't
      maintained anymore, also dropped on mm (see thread on lkml).
    - Moved marvell-ide to patches-to-drop. Because of many ide
      subsystem changes it doesn't apply anymore, and we have already
      pata_marvell so for now it's not critical. We can fix it later if
      desired.
    - Removed some mac80211 wireless drivers that were pushed from old
      wireless-dev tree. We will update later to 2.6.24 that have them,
      and if some driver is still missing we just readd them later.
    - Removed CFS v22 patch, 2.6.23 already have CFS, not with all
      changes but we will update later to 2.6.24 that has all features
      from v22 patch.
    - Removed e1000_7.6.5 patch, we need to check later after update to
      2.6.24 if stock e1000/e1000e is sufficient or if we need to add
      back the driver from intel.
    - Switch from SLAB to SLUB on all kernel configs, SLUB is the
      default since 2.6.23.
    - Drop prefixes for all remaining patches that still used them, now
      that we don't need this anymore. Also fix placement of some
      patches inside series file.

* Mon Oct 15 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.22.10-1.uc2mdv2008.0
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated uvcvideo module to svn-r133 (#34772).
    - Added upstream alsa patch to fix sound issues on Fujitsu-Siemens
      C1410 (#34555).
    - Change laptop flavour to use CONFIG_HZ = 300. Turns out that HZ = 100
      is too low for interactivity, and on laptops it seems it's not worth
      the extra economy of energy (for example, with HZ = 100 there are too
      many audio skips in some applications/games). Reported by Andreas
      Hasenack, and Acked by Luiz Capitulino. We could choose HZ = 250, but
      300 is a bit better in interactivity/less latency and not much a
      difference anyway. And note that accordingly to Len Brown et al paper here:
      http://ftp.kernel.org/pub/linux/kernel/people/lenb/acpi/doc/OLS2006-bltk-paper.pdf
      CONFIG_HZ has a small impact on power consumption on idle workloads,
      so we could even start to think of selecting a HZ = 1000 value for
      laptops where interactivity/less latency is also important (when
      CONFIG_NO_HZ is also available on x86_64 we can switch).

* Mon Oct 15 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.22.10-1.uc1mdv2008.0
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Alsa: fix sound issues on Dell XPS M1210 and M1330 models. The
      oops on M1210 should not happen anymore with upstream alsa hg
      commit 5442 from Takashi Iwai.
    - Fixed mach64 drm support: the existing patch had its build
      disabled because of a bug, and also was broken. Replaced the patch
      with fixed ones (#34473).
    - Updated CFS to version 22.
    - Added Attansic/Atheros(R) L2 Fast Ethernet Adapter driver
      (#34281).
    - Added patch from Emmanuel Andry that adds support for OXCB950
      Cardbus 16950 UART (#33821).
    - Add ipg module from netdev tree (IC Plus IP1000 Gigabit Ethernet
      Adapter).
    - Added upstream alsa bugfix: hda-codec - Fix input_mux numbers for
      vaio stac92xx.

  o Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.22.10
    - readd netfilter ipset, psd & ifwlog support
      (fixes kernel part of: #26376, #29800, #29982, #31402, #32399, #33069)
    - update kernel-laptop descriptions and summary (#33518)
    - disable mrproper target on -devel rpms to stop 3rdparty installers from 
      wiping out needed files and thereby breaking builds (#34672, #34669) 
      (based on an initial patch by Danny used in kernel-multimedia series)
    - add support for ENE CB712/4 card readers (#30172)
    
* Wed Sep 26 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.22.9-1mdv2008.0
  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - 2.6.22.9
    - Revert DU21_remove_anydata_e100a_from_option.patch: just removing the ID
      doesn't fix the real problem and break working devices (see #31631 for more
      information).

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - bcm43xx: fix log flooding with ifplugd when firmware is not
      available (#33969)
    - Add quirk to disable ISOC transfers for device
      "ID 1131:1001 Integrated System Solution Corp. KY-BT100 Bluetooth
      Adapter" (#30638)
    - Add upstream fix "libata: clean up horkage handling". Probably
      needed to really fix #32076, and we must apply it anyway after
      adding BROKEN_HPA horkage support patch
    - x86_64 config:
      * enable p4-clockmod module support, reported by Per �yvind Karlsen;
      * enable abit uguru sensors module.

* Mon Sep 24 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.22.7-1mdv2008.0
  o Thomas Backlund <tmb@mandriva.org>
    - update drbd to 8.0.6 (#33105)
    - disable the AnyData cdma id from option module as it does not work (#31631)
    - fix AppArmor return-code and rejected_mask (from John Johansen @ suse)
    - have only full kernel-source provide /usr/src/linux symlink

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - PCI: Fix boot-time hang on G31/G33 PC (#31632 thanks to Pacho Ramos)
    - Enable drbd compilation on kernel-server

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated to 2.6.22.7, security fix only release (CVE-2007-4573).
    - Upstream bugfixes/new ids from 2.6.23-rcX:
      * intel-agp: Fix i830 mask variable that changed with G33 support;
      * pci: fix unterminated pci_device_id lists;
      * i386: Use global flag to disable broken local apic timer on AMD
        CPUs. This seems to fix a real issue here, without this patch
        a turion laptop gets apic/interrupt errors and misc kernel
        panics;
      * pata_marvell: Add more identifiers;
      * libata: Update the blacklist with a few more devices;
      * ahci: add ATI SB800 PCI IDs;
      * myri10ge: Add support for PCI device id 9.
    - Alsa updates: add missing support for ASUS A7J and nvidia MCP79 to
      hda_intel driver (from alsa repository, reported by Thierry Vignaud).
    - Included ipw3945 in kernel: as reported by many users works better
      than current iwl3945 we use, and we can keep both with current
      mandriva ldetect/module-init-tools (preferred aliases). As talked
      with Olivier Blin seems the better approach right now.
    - Fixed /usr/src/linux symlink check when removing kernel-source
      package, as reported by Andrey Borzenkov on kernel-discuss ML.
    - Enable build of kernel-doc package, reported by Pacho Ramos on
      Cooker ML.

  o Olivier Blin <blino@mandriva.com>
    - enable Conexant 2388x (bt878 successor) support on x86_64

* Wed Sep 19 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.22.6-3mdv2008.0
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - create_configs (config_x86_highmem): implement support for highmem
      64GB setting (closes #33585). Also it's needed to set
      I2O_EXT_ADAPTEC_DMA64 when using it.
    - Added back wireless acx driver (#31539). Thanks to Adam Pigg and
      Adam Williamson for pointers and help.
    - Updated alsa subsystem again, with more bugfixes and new hardware
      support, matches closely alsa 1.0.15rc2 (#33489). Also added some
      more updates after it from hg repository:
      * add support for Asus M2A-VM HDMI and Abit IP35-PRO;
      * sc6000 minor fixes;
      * Dell laptop updates.
    - Upstream bugfixes/enhancements (already in 2.6.23-rcX):
      * ATA device blacklist additions (drives with NCQ/DMA issues);
      * Bugfix for DMA mode on VT6421 PATA port;
      * PATA support for VIA VX800;
      * 945/965GME and G33 intel-agp fixes;
      * Fix broken pata_via cable detection;
      * pata_sis timing fixes;
      * pata_it821x: fix lost interrupt with atapi devices;
      * ata_piix: add sata support for Intel Tolapai;
      * more pata_hpt{37x|3x2n} clock fixes;
      * sata_mv: add pci ids for Hightpoint RocketRaid 1740 and 1742;
      * pata_cs5520: fix probe bug regression introduced in 2.6.22;
      * usb storage: updates/additions to unusual_devs.h;
      * USB: fix support for Dell Wireless Broadband (aka WWAN);
      * forcedeth: add mcp73 support;
      * forcedeth: don't rely on bios to get MAC address order, this
        fixes problems with broken bioses on some Asus boards (like M2N)
        and possibly others;
      * VIA P4M900 support for via-agp;
      * drm/via: Fix dmablit when blit queue is full
        (http://bugs.freedesktop.org/show_bug.cgi?id=11542);
      * usb device additions (new id/support): Samsung X180 China
        cellphone, cdc subset support for Mavell vendor/product ID,
        HUAWEI E220 HSDPA modem, ACER S10 palm device (visor), Dell
        HSDPA 5520;
      * fmvj18x_cs, pcnet_cs: new ids of lan&multifunction cards (NEC
        PK-UG-J001, Panasonic CF-VML201 Panasonic TO-PDL9610,
        MICRO-RESEARCH MC336LAN);
      * sisusbvga: add product ID for Targus ACP50US;
      * run k8t_sound_hostbridge quirk only when needed;
      * unhide SMBus on Compaq Deskpro EP 401963-001 motherboard;
      * ftdi_sio: support new product based on the FTDI 232R USB/Serial;
      * ata_piix: fix pio/mwdma programming;
      * jmicron: PIO fixes (thanks to Thierry Vignaud for pointing
        this), can fix #33043.
    - Fix warning when deregistering acpi dock module (#32337). Added
      patches already upstream, thanks to Danny Tholen for tracking one
      of the commits.

  o Thomas Backlund <tmb@mandriva.org>
    - Really fix /usr/src/linux symlinking on devel rpms (#33559)
    - update unionfs to 2.1.3

  o Olivier Blin <blino@mandriva.com>
    - unionfs: do not update mtime if there is no upper branch for the inode 
      (fix bug with live systems)

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - kernel-server: defaults number of uarts to 32 (#24924)

* Thu Sep 06 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.22.6-2mdv2008.0
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Fixed bug in CE02_acpi-dsdt-initrd-v0.8.4-2.6.21.patch: don't load
      initrd twice, as this causes unpredicted behavior
    - Added some fixes for iwlwifi and b43, from wireless-dev
    - Added patch for kvm that fixes solaris guests (upstream sf.net
      bug #1773613)
    - Add two more ids for some zd1211rw wireless devices, commits from
      wireless-dev tree
    - Added bugfixes and Eagle IV support to ueagle-atm, as reported by
      Olivier Blin on kernel-discuss ML.

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - libata: implement BROKEN_HPA horkage and apply it to affected drives
      (#32076)
    - pata_hpt37x: Fix 2.6.22 clock PLL regression (thanks to Pacho Ramos)
    - USB: add unusual_devs for Nikon devices D50, D80 and D100
      (thanks to Pacho Ramos)
    - USB: Adding support for HTC Smartphones to ipaq (thanks to Pacho Ramos)
    - Fix prefix on FS4 and FS5 (should be FS04 and FS05 respectively), also
      some minor changes in the series file
    - hda-intel: fix codec detection (thanks to Danny Tholen)

  o Thomas Backlund <tmb@mandriva.org>
    - fix AppArmor syslog logging (AppArmor svn rev 961)
    - readd linux prefix to kernel source/devel tree in /usr/src (#33239)
    - readd /usr/src/linux symlink pointing at latest installed 
      source/devel rpm (#33239)

* Tue Sep 04 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.22.6-1mdv2008.0
  o Thomas Backlund <tmb@mandriva.org>
    - add obsoletes/provides to the -latest virtual rpms to allow automatic
      updating to the new kernel-flavours (Big thanks to Anssi for the help):
      * kernel-desktop586-latest obsoletes/provides kernel-legacy-latest
      * kernel-desktop-latest obsoletes/provides kernel-latest
      * kernel-server-latest obsoletes/provides kernel-enterprise-latest
      * kernel-desktop-devel-latest obsoletes/provides kernel-source-stripped-latest
    - update to kernel.org 2.6.22.6
    - update AppArmor to 2.1.0 prerelease (SuSe 10_3 branch, commit 942)
    - redo unionfs AppArmor vfs buildfix (initial patch for 2.1 by 
      John Johansen <jjohansen@suse.de>
    - enable USB_SUSPEND only on laptop kernels, as it causes to much
      regressions for normal users, but is a tradeoff for laptop users (#33089)

  o Pixel <pixel@mandriva.com>
    - Call installkernel without -L since we are the main kernel

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - ext3/4 orphan list debug support and corruption fix (#32527)
    - drop lguest: current version is buggy, and it would take sometime to
      get it in good shape (missing user-space support too)

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Disabled ath5k module, doesn't work now for release, conflicts
      with madwifi.

* Thu Aug 30 2007 Luiz Capitulino <lcapitulino@mandriva.com.br> 2.6.22.5-1mdv2008.0
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Updated to version 2.6.22.5, drop already applied
      ahci_SB700_support patch
    - Updated alsa to latest 2.6.23 code, dropped already applied
      patches
    - Added back legacy ralink drivers (the ones softmac based)
    - Fixup RTC selection in i386/x86_64/alpha configs:
      * Disabled CONFIG_RTC to allow rtc_cmos to be used. Enable generic
        rtc emulation (plus RTC_UIE emulation) in its place
      * Don't enable CONFIG_RTC_INTF_PROC because it conflicts with
        /proc/driver/rtc already provided by CONFIG_GEN_RTC
      * Enable RTC UIE emulation on dev interface for new rtc framework
    - Drop bcm43xx-pci-neuter patch, bcm43xx allowed to all supported
      devices again as module selection will be ldetect's task
    - Removed disable-zd1211rw-mac80211 patch, just disable
      zd1211rw-mac80211 in config instead (zd1211rw more uptodate, no
      need to keep it enabled)
    - Updated wireless subsystem to latest wireless-dev
    - Updated kvm to version 36

  o Luiz Capitulino <lcapitulino@mandriva.com.br>
    - USB: add the ZTE ZXDSL 852 device ID for cxacru (#32707)

  o Thomas Backlund <tmb@mandriva.org>
    - update CFS scheduler to v 20.5
    - update lguest patch for new CFS scheduler
    - drop add-above-background-function patch, merged in CFS
    - update unionfs to 2.1.2
    - update acer_acpi to 0.7
    - use defconfig-desktop as default configs/arch.config, and simplify
      create_configs script accordingly
    - drop xen, xbox and boot support from create_configs as the
      kernel spec does not support them either anymore
    - add virtual kernel rpm for the installer to automatically
      install the default kernel-desktop rpm
    - fix #29744, #29074 in a cleaner way by disabling the sourcing of 
      arch/s390/crypto/Kconfig
    - update kernel descriptions and summarys
    - make kernel-doc name unversioned
    - spec cleanups and typo fixes
    - drop alpha, ia64 support

* Fri Aug 24 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.22.3-1mdv2008.0
  o Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - More wireless updates, fixes/changes for b43 module and ssb from
      wireless-dev
    - Don't allow bcm43xx and b43 coexist for same devices, limit the
      set of devices supported to only one module (patch from fedora)
    - Disable zd1211rw-mac80211 module, use only zd1211rw (to avoid the
      same case like b43 x bcm43xx, and zd1211rw probably is more
      stable)
    - Update ACPI battery and ec with changes that will come in 2.6.23,
      battery update fixes battery reading status deadlock on some
      notebooks when the machine is turned on without ac cable

  o Thomas Backlund <tmb@mandriva.org>
    - change to kernel-tmb spec and naming and kernel.org versioning
    - adapt scripts and Makefile to the new naming scheme

* Thu Aug 16 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.22-6mdv2008.0
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated wireless subsystem to the current state of upstream Linus
      git and wireless-dev, also this obsoletes some previous added
      patches
    - Added external ssb support for b44
    - Added patch for http://bugzilla.kernel.org/show_bug.cgi?id=7995
      (don't restore reserved memory after hibernation, otherwise some
       ACPI status changes while suspending to disk couldn't be updated)

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - HID: fix autocentering of PID devices (Anssi Hannula <anssi@mandriva.org>)
    - Really use CFQ as the default I/O scheduler (trem <trem@mandriva.org>)

  o Thomas Backlund <tmb@mandriva.org>
    - add patch AB03: update to kernel.org 2.6.22.3
    - add patch DN03: fix Realtek id due to upstream nVidia PHY renaming.
    - add patch DS02: fix amd sb700 and add sb800 smbus support (#32568)
    
* Fri Aug 10 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.22-5mdv2008.0
  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Updated iwlwifi to the latest git snapshot
      (06deb1b0e1b9f44ac38c0b0c23a9bb715bb4224f)

  o Thomas Backlund <tmb@mandriva.org>
    - add patch AB02: kernel.org 2.6.22.2
    - drop patches CE07, DI11, HR01, SR01: merged upstream
    - rediff patch SA03 to work with 2.6.22.2

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Use CFQ as the default I/O scheduler

* Wed Aug  8 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.22-4mdv2008.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - e1000: Update to 7.6.5 (#32324)

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Provide pci_ids.h to user space, needed by ldetect, reported by
      Thierry Vignaud
    - Fix issue of some r8169 boards not activating link, using patch
      posted on netdev ML by Francois Romieu (r8169_link_down_fix patch)
    - Disabled CONFIG_DEBUG_SHIRQ on arches where it was enabled, as
      this can cause problems with some modules, like r8169 (see
      https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=242572)
    - update_configs: fix usage typo

  o Thomas Backlund <tmb@mandriva.org>
    - disable DEBUG_SLAB, as it's bad for performance, especially
      under heavier loads
    - add patch AI01: picopower irq router support
    - add patch AI02: Toshiba Equium A60 needs pci=assign-busses (#18989)
    - fix kernel-source-stripped symlinks generation when the -stripped rpm 
      is installed before the kernel (#32236)
    - add patch CE07: fix acpi dock unload oops (#32337)

* Tue Jul 31 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.22-3mdv2008.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - x86_64: Enable saa7134 drivers (#16206)
    - SMBus: Support for AMD/ATI SB700 chipset (#31450)
    - AHCI: IDs for ATI SB700 (#31884)

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Fix for 'make prepare' not working anymore on
      kernel-source-stripped after addition of lguest patch (#31958)
    - Added upstream patch "Add a PCI ID for santa rosa's PATA
      controller"
      (DI11_Add-a-PCI-ID-for-santa-rosa-PATA-controller.patch)

* Fri Jul 20 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.22-2mdv2008.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Usb-audio: another Logitech camera/microphone ID match
      (patch from Daniel Drake <dsd@gentoo.org>)
    - hda-codec: Add quirk for Asus P5LD2
      (path from Claudio Matsuoka <cmatsuoka@gmail.com>)

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Added SR01_serial_reg-header.patch, to export serial_reg.h to user
      space, needed at least for xosview
    - Added "cherry-picked" upstream hrtimers fixes from
      http://www.tglx.de/projects/hrtimers/2.6.22/broken-out/:
      HR01_i386-hpet-check-if-the-counter-works.patch
      HR02_timekeeping-fixup-shadow-variable-argument.patch
      HR03_clockevents-fix-resume-logic.patch
      HR04_clockevents-fix-device-replacement.patch
      HR05_i386-pit-stop-only-when-in-periodic-or-oneshot-mode.patch

* Sun Jul 16 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.22-1mdv2008.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - 2.6.22 rebase
    - lguest
    - CFS process scheduler
    - Lots of 5.1 sound fixes from Claudio Matsuoka (claudio@mandriva.com)

  o Herton Ronaldo Krzesinski <herton@mandriva.com>
    - Added patch with upstream fixes for eeprom 93cx6
      (MC75_eeprom-93cx6-misc-fixes.patch)
    - Rediffed bootsplash patch, while we don't have a definition about
      dropping it or not
    - Added latest patch additions with descriptions (if available, many
      from kernel-tmb) to series file

  o Thomas Backlund <tmb@mandriva.org>
    - set PHYSICAL_START=0x200000 on x86_64
    - use readlink instead of ls and awk in scripts, as ls broken in
      current coreutils (#31906), this also makes the scripts nicer
    - add patch AB17: fix lguest build on x86_64
    - add patch AB18: CFS update to v20 (from -rt tree)
    - rediff patch CD02: Mandriva console logo
    - add patch DI10: Wacom Bamboo Tablet support (#31831)
    - update patch MC17: update ndiswrapper to 1.47
    - add patch MC18: fix ndiswrapper Kconfig and Makefile
    - add patches MC21, MC22: squashfs buildfixes from kernel-tmb
    - update patch MC49: unionfs 2.0 2.6.22.1-u2
    - add patch MC50: fix unionfs build with AppArmor
    - update patch MC54: acer_acpi to v0.6
    - add patches MC60, MC61: drbd v8.0.4
    - add patches MC70-MC74: updated wireless drivers using the new dscape stack
      * ADMtek ADM8211, Broadcom BCM43xx, Iwlwifi, Prism64 PCI, USB
      * Ralink rt2400, rt2500, rt2500 usb, rt61, rt73
      * Realtek 8187 USB, ZyDAS ZD1211/ZD1211B USB
    - drop patch NA01: old drbd version
    - add patches MS01-MS07: Swap Prefetch
    - add patches SA01-SA44: Novell AppArmor 2.0.2 build 755
    - update defconfigs
    
* Fri Jul 06 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.21-4mdv2008.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Makes kernel-source usable again for dkms packages
      (patches from Olivier Blin <blino@mandriva.com>)

* Wed Jul 04 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.21-3mdv2008.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - CFS process scheduler v18
    - Fix kernel-stripped package (from Thomas Backlund <tmb@mandriva.org>)
    - First round of dropped patches, moved 26 into the 'patches-to-drop' queue
    - Rediffed several patches that doesn't apply cleanly
    - Enabled CONFIG_SECURITY and friends
    - Disabled CONFIG_IRQBALANCE (looks like it drops battery life #31725)
    - Alsa HDA codec fixes: 5.1 output on LG LW20 and HP Spartan quirk
      (from Claudio Matsuoka <cmatsuoka@gmail.com>)
    - Alsa usbaudio quirk for Roland Juno-G
      (from Claudio Matsuoka <claudio@mandriva.com>)

* Thu Jun 28 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.21-2mdv2008.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - 2.6.21.5mdv (see the patch file for more info)
    - Drop XEN
    - Drop RSBAC
    - Fix drbd provides (we're providing api = 86 now)
    - kernel-source fixes (some bits from Thomas Backlund <tmb@mandriva.org>)
    - Drakxtool conflict (patch from Thierry Vignaud <tvignaud@mandriva.com>)

* Wed Jun 20 2007 Arnaud Patard <apatard@mandriva.com> 2.6.21-1mdv2008.0
  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.21 upgrade

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Minor build fix
    - Disable XEN build

* Tue Mar 27 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.17-14uc1mdv2007.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - PCI: pcieport-driver: remove invalid warning message

  o Arnaud Patard <apatard@mandriva.com>
    - Fix error path in usbcore
    - Don't build KVM on Xen kernels

* Fri Mar 23 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.17-13mdv2007.0
  o Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - Improve keyboard handling on Apple MacBooks

  o Arnaud Patard <apatard@mandriva.com>
    - Add -latest patch
    - Workaround a possible binutils bug in smp alternatives

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - MCP61: Add forcedeth support
    - Fix potential deadlock in driver core, this issue seems to cause USB
      hangs at boot time (#24683 Thanks to Danny danny@mailmij.org)
    - Security fix:
      * ZZ23_CVE-2007-1592_ipv6_fl_socklist_inadvertently_shared_fix.patch
        (#29821)

* Wed Mar 14 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.17-12mdv2007.0
  o Arnaud Patard <apatard@mandriva.com>
    - Suspend to disk speed improvements
    - Add nmi watchdog support for core2
    - Add atl1 driver
    - Update KVM (rev 4486 + selective changes)
    - Add acer_acpi
    - Update asus_acpi
    - Fix suspend on r8169, i8259A
    - Fix suspend when using ondemand governor
    - Add ide acpi support
    - Add suspend/resume support for sata_nv chipsets.

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Rename ZZ65 patch to ZZ17 and ZZ99 patch to ZZ18 (just to make my
      scripts' life easier)
    - USB: Let USB-Serial option driver handle anydata devices (#29066)
    - USB: Add PlayStation 2 Trance Vibrator driver
    - Fix bogus delay loop in video/aty/mach64_ct.c (thanks to
      Per �yvind Karlsen)
    - Add MCP61 support (#29398 thanks to Pacho Ramos
      pacho@condmat1.ciencias.uniovi.es)
    - USB: fix floppy drive SAMSUNG SFD-321U/EP detected 8 times bug
      (thanks to Ednilson Miura <miura@mandriva.com>)
    - Security fixes:
      * ZZ14_CVE-2007-0958_unreadable_binaries_pt_interp_fix.patch   (#28757)
      * ZZ15_CVE-2007-0772_nfs_free_wrong_pointer_fix.patch          (#28863)
      * ZZ16_CVE-2006-6056_hfs_null_pointer_fix.patch                (#28690)
      * ZZ19_CVE-2007-0005_cm4040_cs_buffer_overflow_fix.patch       (#28634)
      * ZZ20_CVE-2007-1217_capi_debug_buffer_overflow_fix.patch      (#29067)
      * ZZ21_CVE-2007-1388_ipv6_sockglue_null_ptr_fix.patch          (#29400)
      * ZZ22_CVE-2007-1000_ipv6_getsockopt_sticky_null_ptr_fix.patch (#29401)

* Tue Feb 13 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.17-11mdv2007.0
  o Arnaud Patard <apatard@mandriva.com>
    - Fix SiS sata support for chips on 966/968 bridges
    - Add support for SiS968 bridges to the sis190 bridge
    - Add support for showing blocked tasks through sysrq
    - Add nozomi driver
    - Add UVC driver
    - Fix JMicron cable detection
    - Fix issues in squashfs by updating to 3.2 (#27008)

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - x86_64: Add /proc/config.gz support (CONFIG_IKCONFIG)
    - x86_64: Add stack overflow support. Disabled by default, but it's
      something good to have at hand
    - x86_64: Enable kexec
    - USB: rndis_host: fix crash while probing a Nokia S60 mobile
    - rt2570 should report itself as "rt2570" instead of "rtusb" (#24461)
    - atiixp.c: sb600 ide only has one channel (#28505 - thanks to
      Wolke <wolke.liu@amd.com>)
    - PCI: ATI sb600 sata quirk (#28363 - thanks to Wolke <wolke.liu@amd.com>)
    - read_zero_pagealigned() locking fix (thanks to Hugh Dickins
      <hugh@veritas.com>)
    - Fix umask when noACL kernel meets extN tuned for ACLs
      (thanks to Hugh Dickins <hugh@veritas.com>)
    - PowerPC: Make current preempt-safe (thanks to Hugh Dickins
      <hugh@veritas.com>)
    - Security fixes:
      * ZZ12_CVE-2007-0006_key_serial_number_collision_fix.patch (#28636)
      * ZZ13_CVE-2006-5823_cramfs_zlib_inflate.patch             (#28688)

* Fri Feb 02 2007 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.17-10mdv2007.0
  o Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - Add Ralink RT2571W/RT2671 WLAN USB support (rt73 module)

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Fix sys_msync() to report -ENOMEM as before when an unmapped area falls
      within its range, and not to overshoot (LSB regression)
    - Avoid disk sector_t overflow for >2TB ext3 filesystem
    - USB: workaround to fix HP scanners detection (#26728)
    - USB: unusual_devs.h for Sony floppy          (#28378)
    - Dropped FS06_max-symlink-to-10.patch, this patch adds security issues
      on x86_64 machines and was only needed to create Live CDs (now we
      use unionfs). Thanks to Thomas Backlund, who helped to find the
      patch (#27955)
    - Security fixes:
      * ZZ08_CVE-2006-5749_isdn_ppp_init_reset_state_timer.patch (#27802)
      * ZZ09_CVE-2006-5753_fix_bad_inode_retun_values.patch      (#27958)
      * ZZ10_CVE-2006-6053_ext3_handle_dir_corruption.patch      (#28303)
      * ZZ11_CVE-2006-4814_mincore_fix_user_access_locking.patch (#28373)

  o Arnaud Patard <apatard@mandriva.com>
    - Add preliminary ICH9 support
    - Add TI sd card reader support
    - Add RT61 driver
    - KVM update
    - Fix bttv vbi offset
    - Update RT73 and use the firmware class for RT73

* Wed Dec 27 2006 Arnaud Patard <apatard@mandriva.com> 2.6.17-9mdv2007.0
  o Arnaud Patard <apatard@mandriva.com>
    - ata_piix fix for some ICH8 port configurations.
    - Suspend/resume fixes
    - Add KVM
    - Add flush option for fat filesystems
    - X86_64 core2 rdtsc fix

* Fri Dec 19 2006 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.17-8mdv2007.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Dropped DA16_wacom_acpi_enable_future_usage.patch, it does brake
      CONFIG_ACPI=yes compilation seems non-sense and there's no description
      explaining why it's needed
    - Security fixes:
      * ZZ03_CVE-2006-5173_eflags_reset.patch                      (#26535)
      * ZZ04_CVE-2006-5619_ip6_flowlabel_seqfile_fix.patch         (#27034)
      * ZZ05_CVE-2006-5751_bridge_overflow_fix.patch               (#27538)
      * ZZ06_CVE-2006-6106_bluetooth_add_capi_packet_checks.patch  (#27660)
      * ZZ07_CVE-2006-5757_fs_grow_buffers_infinite_loop_fix.patch (#27033)

* Thu Dec 7 2006 Arnaud Patard <apatard@mandriva.com> 2.6.17-7mdv2007.0
  o Arnaud Patard <apatard@mandriva.com>
    - Add Marvell IDE driver
    - Add a driver for Jmicron chipsets instead of using the generic one
    - Update the sky2 driver to fix some network hang issues

* Tue Oct 24 2006 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.17-6mdv2007.0
  o Samir Bellabes <sbellabes@mandriva.com>
    - backport support for network chipset related to r8169 (r8168/r8169SC)

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - 2.6.17.14
    - Dropped DB40_sd_mmc_2gb.patch (fix also in 2.6.17.14)
    - pccard_store_cis: fix wrong error handling
      (reported by Giuseppe Ghib� <ghibo@mandriva.com>)
    - x86_64: add NX mask for PTE entry
      (patch from Eduardo Habkost <ehabkost@mandriva.com>)
    - Fix snd-hda-intel OOPS (patch from Eduardo Habkost <ehabkost@mandriva.com>)
    - mach64: Explicit initialize some members of the drm_driver structure,
      otherwise NULL init will have bad side effetcs
      (patch from Couriousous <couriousous@mandriva.org>)
    - Adds Missing check for CAP_NET_ADMIN in iptables compat layer
    - Support for building .nosrc.rpm
      (patch from Thomas Backlund <tmb@mandriva.org>)
    - Security fixes
      * ZZ01_CVE-2006-4997_clip_do_not_refer_freed_skbuff.patch           (#26608)
      * ZZ02_CVE-2006-4572_netfilter_ipv6_fragmention_attacks_fixes.patch (#26745)

  o Arnaud Patard <apatard@mandriva.com>
    - Fix pcmcia unplug/eject on cards with r8169 chipsets
    - Fix libata resource conflicts detection (#23279)
    - Fix xenU crash and reenable domU boot logs.
    - Fix refcount error triggered by softwares using /proc/<pid>/auxv

* Wed Sep  6 2006 Arnaud Patard <apatard@mandriva.com> 2.6.17-5mdv2007.0
  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.17-13
    - RSBAC fixlets
    - Fix JMicron SATA/PATA chipsets support (#25155)
    - Update the at76c503a usb driver (now called at76_usb) (#25278)
    - Fix reversed error test in netif_tx_trylock (#25249)
    - Fix modalias on 64bits (#25431)
    - Fix ipmi_msghandler oops on removal (#25463)
    - Replace DU04 with its upstream version
    - Disable MSI on azalia codecs to prevent IRQ troubles.
    - Disable FN keys in the i8k driver when failing to get the dell smm bios
    version. Patch from Per Oyvind Karlsen. (#21140)

  o Samir Bellabes <sbellabes@mandriva.com> 
    - cosmetic changes from Thomas Backlund <tmb@mandriva.org>

* Mon Sep 4 2006 Arnaud Patard <apatard@mandriva.com> 2.6.17-4mdv2007.0
  o Samir Bellabes <sbellabes@mandriva.com> 
    - netfilter fix - bug #24252
    - fix netfilter IFWLOG

  o Arnaud Patard <apatard@mandriva.com>
    - AHCI suspend
    - Squashfs 3.1r2
    - Fix oops on video.ko rmmod
    - SiS 966 chipsets support
    - Add support for 2Gb memory cards
    - Fix uhci list bug
    - Revert reset changes in the e1000 driver. This should fix
    the e1000 resume issues
    - Fix list usage in the sis190 driver

* Mon Aug 29 2006 Arnaud Patard <apatard@mandriva.com> 2.6.17-3mdv2007.0
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Updates drbd to 8.0pre4
    - Adds drbd-api provides (#24264)
    - Adds support for partitioned loop devices (patch from Flavio
      fbl@mandriva.com)
    - Fix double ACPI video /proc entries (patch from Danny danny@mailmij.org
      #22249)

  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.17.11
    - Alsa 1.0.12
    - Enable USB_EHCI_SPLIT_ISO (#24412)
    - Fix sparc build (#24646)
    - Fix Xen on 32bit and workaround Xen bug on 64bit.
    - Fix b44 module (#24312)
    - RSBAC 1.2.8
  
* Thu Aug 10 2006 Arnaud Patard <apatard@mandriva.com> 2.6.17-2mdv2007.0
  o Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - Enable HUGETLBFS
    - Factor out configs

  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.17.8
    - Alsa 1.0.12rc2
    - Add usb ids for the Testo usb device (bug #23666)
    - Add quickcam messenger driver for 2.6.18-rcX
    - ata_piix/ICH8 fixes
    - ACL support for tmpfs  (bug #24045)
    - Add DI20_initialize_hw_regs_in_setup_ports.patch from 2006-upd
    - i965 support
    - Intel iAMT redirection drivers

  o Samir Bellabes <sbellabes@mandriva.com>
    - Add support for chipset realtek 8168. (bug #23705)
    - Add netfilter ipset patch
    - Add netfilter conntrack/nat sip patch
    - Add netfilter psd patch

* Tue Jun 29 2006 Arnaud Patard <apatard@mandriva.com> 2.6.17-1mdk
    - 2.6.17.6
    - Alsa 1.0.12rc1
    - Rsbac 1.2.8(pre1)
    - New Xen snapshot
    - New wireless-2.6 snapshot (adds zd1211rw driver)
    - KGDB drop
    - e100, e1000 update
    - Via VT8251 sata support
    - vt_ar5k drop. Considered as obselete by upstream.
    - svgalib_helper drop.
    - 3rdparty updates : acerhk, drbd, dxr3, ipw3945, ivtv, lirc,
    mod_marvel, ndiswrapper

* Wed Jun 28 2006 Samir Bellabes <sbellabes@mandriva.com> 2.6.16-3mdk
  o Samir Bellabes <sbellabes@mandriva.com>
    - re-enable supermount (fix bug #23217)
    - ct_sync aka 'howto replicate the firewall'

* Mon May 22 2006 Arnaud Patard <apatard@mandriva.com> 2.6.16-2mdk
  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.16.20
    - input.h : move input_device_id to mod_devicetable.h
    - Reenable unintentially disabled unionfs
    - RS02/RS11 cleanup
    - Removed bcm4400. We have the b44 module in the kernel
    - Fix usage of acpi_clear_event() in CE06
    - Enable cpufreq on SMP, disable USB_BANDWIDTH
    - Build smp and up kernel on sparc (Peroyvind)
    - Switch to GENERIC_ARCH on x86 to suppress the false warning
    about the number of cpus when using cpu hotplug
    - Add xen0 support in rhconfig.h
    - Fix freeze when using the 'live' mode of gi (instead of using the 
    clp files)
    - Activate RSBAC_INIT_DELAY to get rsbac working with all kind of
    initrd/initramfs
    - Fix fdomain vs x86_64/isa trouble

* Thu May 11 2006 Arnaud Patard <apatard@mandriva.com> 2.6.16-1mdk
  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.16.16
    - Wireless update (Adds the bcm43xx driver)
    - mmc layer update (Adds the sdhci driver)
    - e1000 update
    - Xbox support outdated, so (temporary ?) removed
    - Alsa 1.0.11
    - RSBAC 1.2.6
    - New Xen snapshot
    - Updated 3rdparty
    - ipw3945

* Mon Mar 13 2006 Eduardo Pereira Habkost <ehabkost@mandriva.com> 2.6.14-2.1mdk
  o Eduardo Pereira Habkost <ehabkost@mandriva.com>
    - Change kernel-source version field to 1-1mdk, like the rest of
      the versioned packages

* Fri Mar 10 2006 Eduardo Pereira Habkost <ehabkost@mandriva.com> 2.6.14-2mdk
  o Eduardo Pereira Habkost <ehabkost@mandriva.com>
    - Avoid automatic update of kernel-source without updating the kernel:
      - Put package version on package name for kernel-source and
        kernel-source-stripped
      - Remove Obsoletes: kernel-source from kernel-source* packages
      - Closes: #21345

  o Samir Bellabes <sbellabes@mandriva.com>
    - update ipt_IFWLOG (interactive firewall)

  o Arnaud Patard <apatard@mandriva.com>
    - Fix bad update of RS11
 
* Mon Feb  7 2006 Arnaud Patard <apatard@mandriva.com> 2.6.14-1mdk
  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.14.7
    - Alsa 1.0.10 and cvs update.
    - Xen update from the linux-2.6 tree. Build it now as a machine and no more
      as a different architecture.
    - Rsbac 1.2.5
    - Drbd 0.7.15
    - The bcm5700 driver is no more supported by Broadcom, thus dropping it.
    - Dropped the now merged ipw2100, ipw2200, ieee80211, fuse, hostap 3rdparty
      tarballs.
    - Changed the eagle-usb driver in favour of the to-be-merged version
    - Use now the acx driver from akpm's tree.
    - Update 3rdparty drivers : lirc, ndiswrapper, rt2400, rt2500 
    - Added rt2570 usb driver.

  o Samir Bellabes <sbellabes@mandriva.com>
    - netfilter update (DN30_netfilter_svn6470.patch)
    - unionfs 1.1.3

* Thu Nov 24 2005 Luiz Capitulino <lcapitulino@mandriva.com> 2.6.12-13.1mdk
  o Arnaud Patard <apatard@mandriva.com>
    - Fix oops when reading /proc/driver/pktcdvd/pktcdvd0

  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Added DA75_alsa_patch_realtek_fix.patch to fix a bug which makes
      some sound-cards managed by snd-hda-intel useless
 
* Mon Nov 21 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.6.12-13mdk
  o Luiz Capitulino <lcapitulino@mandriva.com>
    - Updated pl2303 usb-serial driver to support X75 and SX1 Siemens mobiles

  o Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - power5 & pmac64 support
    - selected fixes from 2.6.13 and beyond:
      * add r300 drm support
      * fix x86_64 idle=poll
      * fix races in libata core
      * properly fix the radeon IRQ handling code
      * properly fix the errata #122 workaround on x86_64 + add it to i386
      * merge new upstream ioctl32 compat code, thus supporting i915 as well

  o Arnaud Patard <apatard@mandriva.com>
    - Fix typo in the SiS965L support. Restore the right address for the other chipsets.

* Thu Sep  8 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.6.12-12mdk
  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.12.6
    - Removed lpfc from 3rdparty as it exists in drivers/scsi/ (Thanks Svetljo 
      for pointing out this).
    - Added sata_sil24 module
    - Added SiS182 minimal support.
    - Added SiS190 driver.
    - Added support of the IDE chipset of the SiS965L boards.
    - Added various pciids from 2.6.13
    - Removed patch MD48. Now we're using udev, it breaks the prism2 module
    - Inotify fixlets
    - Removed the patch that disable the smm bios and use usb-handoff by default (Sveltjo)
    - USS725 fixes (Sveltjo)
    - execve LSB test fix (Stew)
    - Via unichrome support update (Danny)

  o Samir Bellabes
    - Add DN34_nf_rsh-conntrack_timeout.patch : 
      Fix timeout for ip_conntrack_rsh (bug #17368)
    - backport fixes for netfilter from 2.6.13-git8: (DN60-DN75 + DN80)
      * check hardware checksum in ECN, queue, TCPMSS
      * fix tcp checksum in ipt_REJECT
      * ipt_CLUSTERING: deletion, ct_related, mangling arp, memcpy_typo
      * ip6table_raw: missing owner
      * race condition in Decnet
      * optimize expected timeout
      * delete reference conntrack in ipmr
      * fix ECN tcp marking
      * fix byteorder in icmp NAT
      * fix ip6t_LOG sit tunnel logging 
      * fix masquerading index for slave connection
      * fix sysctl_tcp_low_latency
      * IFWLOG : fix bad kfree and close bug #18276 (DN33_netfilter_IFWLOG.patch)
    - Fix buffer overflow with module_param (DN76_nf_bad_param_port.patch)
      
  o Flavio Bruno Leitner <flavio@mandriva.com>
    - XEN updated to 2005-08-23

  o Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - increase number of supported CPUs to 32
    - add workaround for x86_64 errata #122
    - update PowerNow!K8 driver to v1.50.3 for rev.F Opteron support

* Sun Aug 28 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.6.12-11mdk
- remove obsolete patches that were fixed differently
- assorted x86_64 fixes from current git tree:
  * fix 32-bit thread debugging
  * fix TASK_SIZE for compatibility mode processes
  * fix overflow in NUMA hash function setup
  * fix bug in csum_partial_copy_generic()
  * fix HPET for systems that don't support legacy replacement
  * add support for more than 8 cores on AMD64 systems
  * tell VM about holes in nodes
  * avoid wasting IRQs

* Mon Aug 15 2005 <flavio@mandriva.com> 2.6.12-10mdk
  o Flavio Bruno Leitner <flavio@mandriva.com>
    - WARNING: Security
      Hyper-Threading enabled by default. 
      (at boot time use ht=off to disable)
    - applied patch to cpufreq support centrino.
    - updated ibm_acpi to 0.11
    - fixes to NFS
    - ACL support to NFS
    - XEN configs updated (enabled more options)

  o Samir Bellabes <sbellabes@mandriva.com>
    - 2.6.12.5

  o Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - fix inotify 0.24 patch
    - fix build of ndiswrapper 1.2 on x86_64
    - only build xen on x86, will enable on x86_64 later

* Thu Jul 28 2005 Arnaud Patard <apatard@mandriva.com> 2.6.12-9mdk
  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.12-4
    - Advertise the megaraid_mbox as megaraid_mbox (and not megaraid) in sysfs
    - Ndiswrapper 1.2
    - Updated ipw2100 to 1.1.2, ipw2200 to 1.0.6 
    - e100 and e1000 drivers update (e100 to 3.4.8-k2 and e1000 to 6.0.60-k2)
    - inotify 0.24
    - Set the pwc driver to use non compressed mode by default.

  o Samir Bellabes <sbellabes@mandriva.com>
    - Add MD40_rt2500_local_bh_enable_fix.patch
    - Add DN33_netfilter_IFWLOG.patch (Interactive Firewall)

  o Flavio Bruno Leitner <flavio@mandriva.com>
    - use mkinitrd without -C to force cramfs, let mkinitrd decide it.
    - add requires to module-init-tools instead of old modutils.
    - added XEN support

  o Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - resurrect legacy megaraid for { 0x9010, 0x9060, 0x1960 } (Pascal)

* Tue Jul 26 2005 Flavio Bruno Leitner <flavio@mandriva.com> 2.6.12-8mdk
  o Flavio Bruno Leitner <flavio@mandriva.com>
    - reverted latest standard wireless extensions update to v18
      (v19 isn't compatible with previous and/or maybe incomplete)
    - disabled know broken qlogicisp. (superseded by the qla1280 driver)

  o Arnaud Patard <apatard@mandriva.com>
    - 2.6.12.3. Removed the AC01 patch as 2.6.12.3 provide it.

  o Samir Bellabes <sbellabes@mandriva.com>
    - Remove DN31_netfilter-rtsp-20040302.patch (updated in DN32_netfilter_050725.patch)
    - Add DN30_kill_lockhelp.patch (use lock directly)
    - Add DN31_kill_nf_debug.patch (don't use NETFILTER_DEBUG anymore)
    - Add DN32_netfilter_050725.patch (details in svn log)

  o Gwenole Beauchesne <gbeauchesne@mandriva.com> 
    - merge and fix drm ioctl32 compat code (x86_64)

* Mon Jul 07 2005 Flavio Bruno Leitner <flavio@mandriva.com> 2.6.12-7mdk
  o Flavio Bruno Leitner <flavio@mandriva.com>
    - WARNING: removed patch to rename kernel modules 
      (Closes ticket #13428)
    - updated standard wireless extensions to v19
      (DN55_iw_we18-5.diff, DN56_iw262_we19-9.diff)
    - added support for Avermedia AVerTV GO 007 FM
      (DV52_avermedia.patch)
    - fix TPM to use BIOS instead of hardcoded memory address.
      (AC01_tpm-memory-fix.patch)

  o Arnaud Patard <apatard@mandriva.com>
    - updated to alsa 1.0.9b
    - Removed DA54_add-to-snd-intel8x0-ac97-quirk-list.patch as it has been merged.
    - inotify update to 0.23-2.6.12-15
    - Reenabled software suspend.
    - Bluez update (to 2.6.12-mh1). It adds a better HID support in bluez
    stack
    - Fixed and enable the ppscsi driver.

* Mon Jul 07 2005 Flavio Bruno Leitner <flavio@mandriva.com> 2.6.12-6mdk
  o Arnaud Patard <apatard@mandriva.com> 
    - Add support for newer versions of wpa_supplicant
    - added fixes for ipw2[12]00 drivers
    - sk98lin v8.23.1.3
    - added USB id of the Gigabyte GN-WLBZ101
    - enabled FATX support for xbox
  o Flavio Bruno Leitner <flavio@mandriva.com>
    - updated orinoco to 0.15rc2. 
    - updated to 2.6.12.2
    - enabled advansys, qlogicisp, eata_pio as module

* Mon Jul 04 2005 Flavio Bruno Leitner <flavio@mandriva.com> 2.6.12-5mdk
- updated to 2.6.12.2
  (added AB02_2.6.12.2.patch)

* Fri Jul  1 2005 Arnaud Patard <apatard@mandriva.com> 2.6.12-4mdk
- Ensure that stallion and istallion modules return an error code instead of 0 
  when something goes wrong.

* Thu Jun 23 2005 Fl�vio Bruno Leitner <flavio@mandriva.com> 2.6.12-3mdk
- new kernel version: 2.6.12.1
- rollback some of removed patches in 2.6.12-1mdk.

* Wed Jun 22 2005 Fl�vio Bruno Leitner <flavio@mandriva.com> 2.6.12-2mdk
- added drbd 0.7.11

* Wed Jun 22 2005 Fl�vio Bruno Leitner <flavio@mandriva.com> 2.6.12-1mdk
- new kernel version: 2.6.12
- updated bootsplash: 3.1.6
- enabled config on /proc. (/proc/config.gz)
- enabled cpufreq conservative module.
- removed ipmi smb support until be fixed for 2.6.12.
- enabled new sensors modules.
- renamed MandrakeSoft to Mandriva. (README.Mandriva too)
- fixed/improved some descriptions.
- don't use tarball for patches and scripts. (svn repos)
- added new patches:
  o MD27_tivatv-agp.patch (agp_copy_info changed)
  o MD56_pci_name-renamed.patch (s/pci->slot_name/pci_name()/)
  o MD55_i2c-client-unused-id.patch (drop unused i2c_client->id)
  o MD54_3rdpart-scsi-legacy.patch (rollback some SCSI defines)
  o JX02_reparent_public.patch (XBOX needs reparent_to_init)
  o MD53_3rdpart-removed-defined-func.patch (gcc4 fix)
  o DV32_via_mach64_drm_fixes.patch (minor field moved)
  o RS13_rsbac-2.6.12.patch (RSBAC needs task_capability_lock)
- removed already applied patches (about 55 patches)

* Mon May 30 2005 Juan Quintela <quintela@mandrakesoft.com> 2.6.11-10mdk
- disable HT by default.
- improved xbox support (stew).
- ext3_journal_unmap_buffer_race.
- CAN-2005-0750_af_bluetooth.
- CAN-2005-0400-ext2_leak.
- CAN-2005-0749_load_elf_library_DOS.
- CAN-2005-1263 binfmt_elf.
- CAN-2005-1264 raw_ioctl.
- CAN-2005-1369 sys_rw_files.

* Mon May 23 2005 Arnaud Patard <apatard@mandriva.com> 2.6.11-9mdk

- Updates: 
  - 2.6.11.10
  - Fixed ndiswrapper Makefile

- Fixes:
  - Fix build with gcc 4.0
  - Fix return codes in do_readv_writev

* Tue Apr 26 2005 Arnaud Patard <apatard@mandriva.com> 2.6.11-8mdk

- Added:
  - endian patches (Sveltjo)
  - Rename ovcam in 3rdparty to ovcam-alt (Sveltjo)
  - Add build fix for the next binutils
  - Support for sata_sil on rs480 (Gb)

- Updated:
  - Updated to 2.6.11.7
  - Lirc 0.7.1. Also fix some broken compile options
  - ipw2X00 update. Corrected also monitor mode for ipw2100.
  - saa7134 update for dvb
  - Compile mkiss as module
  - Ndiswrapper 1.2rc1 (NX support)
  - Build saa7174hl in 3rdparty/video-rivatv

* Sun Apr 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.11-7mdk
- sata_sil updates to v0.9
- disable pin1 APIC timer on RS480 based motherboards (e.g. HP DX5150)

* Tue Mar 22 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.11-6mdk
- enable Intel AGP support for x86-64 again (bk)
- make drm a module on x86_64 for ati drivers to work without hacks
- bring back sheep_net module for raw access to ethernet packets
- fix build on x86_64, aka remove obsolete edid/vbe stuff partly merged

* Mon Mar 21 2005 Juan Quintela <quintela@mandrakesoft.com> 2.6.11-5mdk
- several alsa fixes (arnaud).
- ipw2[12]00 wap fix (arnaud).
- disable SELINUX (we use RSBAC).
- xbox build, update spec, JX01 patch, create_configs (stew).

* Mon Mar 21 2005 Juan Quintela <quintela@mandrakesoft.com> 2.6.11-4mdk
- disable via on amd64 (for same reason does a malloc way too big).
- really compile mach64 drm.

* Sun Mar 20 2005 Juan Quintela <quintela@mandrakesoft.com> 2.6.11-3mdk
- add 2.6.11.4 patch.
- new drm for via-unichrome & ati-match64.
- bttv should work again (it is a bad idea to have two modules with the 
  same name :p ).
- new Chelsio 10GB ethernet.
- new LSI megaraid sas driver.
- compile i686-up-4GB kernel (Dothan don't work with PAE enabled).
- compile BOOT kernel (needed for cdrom yet).

* Thu Mar 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.11-2mdk
- merge with 10.2/x86_64 branch:
  * workaround build with icecream
  * fix ndiswrapper build
  * fix inotify compat32 code
  * fix drm/ioctl32 forward port to 2.6.11
- selected fixes from bitkeeper:
  * make IRDA devices are not really ISA devices not depend on CONFIG_ISA
  * fix boot up SMP race in timer setup on i386/x86-64

* Wed Mar 9 2005 Arnaud Patard <apatard@mandrakesoft.com> 2.6.11-1mdk

 * New kernel version
 * Include rtc in the kernel and no more in module.
 * Fixed the dl2k ethtool.

- Added :
 * usbat2 driver

- Updated :
 * Alsa 1.08 (cvs version of 20050308)
 * Ndiswrapper 1.0
 * Inotify 0.20-2 (still activated in the kernel but support
   disabled in gamin due to stability problems)
 * Bootsplash to 3.1.4-2.6.11
 * RSBAC 1.2.4
 * sk98lin 8.14
 * acx100 0.2.0-pre8 + fixes_46
 * qcusb 0.6.2
 * eagle-usb 2.2.0
 * Prevent building scsi_transport_iscsi module from the iscsi-mod
   as it's now in the kernel

- Removed :
 * AA08_isapnp_interwave.patch as it's in the BK01
   patch
 * old patches from BK (CA01,DI09,DI10,DI11,DI12,DI13,DI14,DI15,
   DI16,FS04)

* Mon Feb 21 2005 Juan Quintela <quintela@mandrakesoft.com> 2.6.10-3mdk
- rsbac is compiled but not enabled by default.

* Sun Feb 20 2005 Juan Quintela <quintela@mandrakesoft.com> 2.6.10-3mdk
  * Fix ata_piix support for ich6-r drives
  * Add ICH7 support
  * Add support for ICHX watchdog support
  * Adding command line option for a configurable delay before mounting
    root
  * Add support for ULi M5288
- Updated :
  * sk98lin
  * inotify to 0.18-rml-2.6.10-16
  * dxr3
  * ivtv to 0.2.0-rc3f
  * ipw2100 to 1.0.5
  * ipw2200 to 1.0.1
  * eagle-usb 2.1.0rc1
  * wlan-ng (prism2) 0.2.1-pre26
- Removed hpusbscsi module
- Renamed old radeon framebuffer driver to radeonfb_old (Sveltjo)
- Added a missing header in the idsn driver (Sveltjo)
- Corrected linux-mdkconfig.h
- Removed some unusefull built-in modules in the boot kernel
- Fixed config for the acerhk module as it builds only on X86 arch
- Xbox support (Stew)
- Add support for a gigabit card from USRobotic.
- Try to use the old usb enumeration scheme before trying the new one
- Add some keycodes for some keyboards made by Cherry
- Added support for the Uli M5263 network card

* Wed Feb  9 2005 Juan Quintela <quintela@mandrakesoft.com> 2.6.10-2mdk
- compile kernels:
  * UP: with NX support
  * SMP: with NX support
  * i586-up-1GB, for machines that don't support PAE.
- kernel-secure is gone, UP & SMP have rsbac as default.
- kernel-BOOT is gone, i586 should be ok for installer
- x86_64 compiles again.
- drm.biarch really integrated, no more symlinks.
- fixed lots of small problems & unused patches.
- create_configs & update_configs work again as expected.

* Mon Jan 10 2005 Arnaud Patard <apatard@mandrakesoft.com> 2.6.10-1mdk
- New upstream version
- Updated alsa with alsa CVS and added drivers from the multimedia kernels
- Updated 3rdparty : 
  * hostap
  * ipw2200
  * fuse
  * ipmi_smb and af_ipmi
  * dazuko
  * iscsi to 4.0.1.11 with a patch to rename strdup present in iscsi-session.c
    to iscsi_strdup
  * opengfs with version from http://sources.redhat.com/cluster/gfs/ 
  exported symbol (sock_getsockopt)
- Added zd1201 driver
- Added inotify
- Dropped MD34_iteraid and DI03_add-support-for-it8212-ide-controllers.patch in favour
  of Alan Cox's version
- Added delkin_cb driver from Alan Cox
- Added some functions that were suppressed from i2c-core as they were not used in 
  vanilla kernel
- Removed all MOD_INC_USE_COUNT and MOD_DEC_USE_COUNT as now it has been 
  suppressed
- Added some missing linux/version.h in alsa drivers in 3rdparty
- Fixed some broken {Kconfig,Makefile} in 3rdparty
- Added a warning when trying to do some scsi command not permitted
- Removed some call to usb_unlink_urb in eagle-usb

* Tue Dec 21 2004 Arnaud Patard <apatard@mandrakesoft.com> 2.6.9-1mdk
- Updated 3rdparty/
- Removed merged upstream patches
- Added Ralink drivers
- Updated libata (ahci support added)

* Mon Nov  8 2004 Juan Quintela <quintela@mandrakesoft.com> 2.6.8.1-21mdk
- fix unitialized skbuf with tso cards.
- CAN-2004-0814 tty_fixes.
- merge again with cooker kernel.
- remove build_acpi (always acpi now).
- fix bug #11262 (alsa mixer oops) (samir).
- Updated ipw2200 (Arnaud).
- Fix Kconfig for qlogic drives (Arnaud).
- Updated libata with fixes from 2.6.10-rc1 to correct cd-rom drives
  detection (arnaud).
- Added a patch to correct multipath problems with qla driver (Arnaud).


* Wed Nov  3 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-20mdk
- revert TARGET_CPUS change on x86_64
- config updates to x86_64:
  * enable Intel CPU microcode support
  * enable AMD 8111 (new PCI lance) support
  * change enhanced real time clock support to be built-in kernel image
  * enable JFS filesystem support
  * enable Intersil Prism GT/Duette/Indigo PCI/Cardbus support

* Thu Oct 28 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-19mdk
- add x86_64 rsbac syscalls
- temporarily re-enable IOAPIC workaround on x86_64/VIA
- selected fixes from kernels up to 2.6.10-rc1:
  * try to recover from bugous USB string descriptors (e.g. Freebox USB)
  * fix off-by-one error in TSS limit on x86_64
  * new megaraid v2.20.3.1 driver
  * add Seagate ST3120026AS to SATA SIL mod15 quirks

* Sat Oct 23 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-18mdk
- selected fixes from 2.6.9:
  * fix pointer dereference before NULL check in ACPI thermal driver
  * change TARGET_CPUS on x86_64 to match x86 mach-default
  * fix the Lindenhurst MSI fix on x86-64 to compile again
  * swsuspend fixes to x86_64
  * fix cardbus card memory assignment on x86_64

* Fri Oct 22 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-17mdk
- re-enable KALLSYMS on x86_64
- merge x86_64 cpufreq configs with i386
- 64-bit fixes to acpi/processor module (2.6.9)
- keep acpi/processor module loaded for powernow-k8 (SuSE)

* Mon Oct 11 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-16mdk
- remove devfs automount config
- revert 82801EB ICH5 IDE changes

* Thu Oct  7 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-15mdk
- enable ACPI and Centrino speedstep for Nocona systems
- selected x86-64 fixes from 2.6.9rc3 tree:
  * don't panic when io apic id cannot be set

* Thu Oct  7 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-14mdk
- fix speedtouch support on 64-bit platforms
- selected x86-64 fixes from 2.6.9rc3 tree:
  * add support for NUMA discovery on AMD dual core to x86-64
  * fix sibling map for clustered mode
  * report PNI support in recent AMD CPUs

* Wed Oct  6 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-13mdk
- fix build of ipc32 compat on x86_64
- fix sata_nv on non-CK8-04 systems (Andrew Chew)

* Thu Sep 30 2004 Juan Quintela <quintela@mandrakesoft.com> 2.6.8.1-12mdk
- Fix Oops on sched_api (fix bug #11322)>
- create i686-up-64GB kernel, idea is having PAE kernels for up & smp 
  (only way to have NX protection).


* Mon Sep 27 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8.1-11mdk
- cpufreq update.
- cpuid update.
- tcp_default_win_scale fix. 
- fix rsbac printk.
- ipw2200 0.8.
- msdos/vfat sync.

* Tue Sep  7 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8.1-10mdk
- bootsplash 3.1.6.
- fix bootsplash vt0 display.
- ipw2100 0.54.
- ipw2200 0.7.

* Tue Sep  7 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.8.1-9mdk
- x86_64 2.6.8-1

* Fri Sep  3 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8.1-8mdk
- remember install use ext2.gz initrd image file.
- don't obsoletes kernel-source-2.6.

* Fri Sep  3 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8.1-7mdk
- drop 8139too rx fifo.
- eagle-usb 1.9.9.
- lastest scsi ioctl.

* Fri Sep  3 2004 Juan Quintela <quintela@mandrakesoft.com> 2.6.8.1-6mdk
- fix right Provides/Obsolets for kernel-source*.
- remove dir /usr/src/linux.
- really, really use cramfs for initrd.
- big config clean-up.
- acpi floppy code removal (Oops should have gone).
- orinoco update to 2.4.9-rc1.

* Fri Aug 27 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8.1-5mdk
- drop atkbd interrupt interaction.
- drop nfs, knfsd patch suites.

* Thu Aug 26 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8.1-4mdk
- more info on new kernels :
  o BOOT (i586 up 1GB optimize for size)
  o up (i586 up 4GB + selinux)
  o smp (i686 smp 4GB + selinux)
  o enterprise (i686 smp 64GB + selinux)
  o secure (i686 smp 64GB + selinux + rsbac)
  o i586-up-1GB (legacy kernel + selinux)
- selinux=0 as default.
- rename s/kernel-source/kernel-source-2.6/ provide kernel-source
	 s/kernel-source-stripped/kernel-source-stripped-2.6/ provide kernel-source-2.6 kernel-source
- acpi 20040715.
- ipmi v3.2 af_ipmi, smb.
- really do cramfs as static in kernel.
- cpufreq, software suspend, drm, libata updates
- add agpgart i915 support.
- usb updates.
- don't detect wacom tablet as mouse (flepied).
- lots of mm selected patches like:
  o it8212 support.
  o aio/bio updates.
  o ext2/ext3/jffs fixes.
  o software suspend fixes.
  o selinux fixes.
  o i810 audio fixes.
  o cd/dvd packet writing updates.
  o posix locking fix.
  o cciss/i2o updates.
  o via-rhine fixes.
  o nfsd fixes.

* Thu Aug 26 2004 Juan Quintela <quintela@mandrakesoft.com> 2.6.8.1-3mdk
- used cramfs for initrd instead of ext2.
- weigth reduction program begins.
- 2.6.8.1-q3.
  * unset PCI_NAMES
  * unset IMSTTT
  * unset all elan options (kernel will not work anywhere).
  * unset IKCONFIG (you have the config file in /boot and in all mandrake 
    mirrors).
  * unset EISA.
  * NFS is now a module again (magic in mkinitrd will fix it in next release).
  * now we have:
      - kernel i586 up 1GB (for old machines)
      - kernel up (i686 up 4GB)
      - kernel smp (i686 smp 4GB)
      - kernel p3 smp 64GB
      - kernel secure (i586 smp 4GB)
      - kernel BOOT (i386 up 1GB)
  * plan is remove also BOOT (if weight reduction program has enough success)
    and secure (if options can be integrated without too much fuss in the 
    others).

* Wed Aug 18 2004 Olivier Blin <blino@mandrake.org> 2.6.8.1-2mdk
- update bootsplash patch (from bootsplash.de)

* Mon Aug 16 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8.1-1mdk
- 2.6.8.1.
- alsa 1.0.6.

* Thu Aug 12 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8-0.rc4.1mdk
- rc4 bk3.

* Wed Jul 21 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8-0.rc2.2mdk
- fix double EXTRAVERSION in Makefile (introduce by rsbac patch vs specfile)
- add tc1100-wmi/wacom_acpi driver for HP/Compaq TC1100 tabletpc. (aacton)
- add ntfs support in BOOT kernel.
- next is from mm patchset.
- lastest agpgart.
- cpufreq for nforce2.
- enable suspend/resuming of e1000.
- i810_audio mmio support.
- dvdrw/cdrw packet writing.
- update drivers net pcmcia/wireless.
- posix locking fix.
- x86-64 support singlestep into 32bit syscalls
- 3rdparty BIG update :
  o acx100-0.2.0pre8.
  o eagle-usb-1.9.8.
  o hostap-0.2.4.
  o lirc-20040406.
  o qc-usb-0.6.0.
  o dfg1394-1.3.
  o prism25-0.2.1.
  o ov511-2.28.
  o iscsi-mod-4.0.1.
  o bcm5700-7.1.22.
  o at76c503a-cvs20072004.
  o ndiswrapper-0.8.
  o acecad-3.1.
  o squashfs_2.0.
  o ivtv-cvs21072004.
  o rivatv-0.8.5.
  o sn9c102-1.02_beta. (w9968cf alternative)
  o fuse-1.3.
  o iteraid-092005-09.
  o shfs-0.35.
  o ipw2100-0.50.
  o ipw2200-0.2.

* Sun Jul 18 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8-0.rc2.1mdk
- rc2.
- really enable codepage 437 in BOOT kernel.
- add rsbac security patch in secure kernel.
- modules.description fix (blino).
- no more modversioning module.
- lufs 0.9.7.
- BadRam.

* Fri Jul 16 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8-0.rc1.2mdk
- dazuko 2.0.2.
- codepage 437 module in BOOT kernel.
- kexec is back. 

* Mon Jul 12 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.8-0.rc1.1mdk
- 2.6.8-rc1.
- bootsplash is back.
- ak series amd64 patchsets (gb).
- piix is back as static.
- ide-generic as module.

* Mon Jun 21 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.7-2mdk
- bluetooth mh1.
- mppe mppc 1.0. (florin request)

* Thu Jun 17 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.7-1mdk
- 2.6.7.

* Mon Jun 14 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.7-0.rc3.1mdk
- rc3.
- bk5.
- kdb 4.4 (i386 ia64 x86_64).
- drop bootsplash for the moment.
- disable pata piix driver, enable generic ide, enable PATA ATAPI in libata.

* Wed Jun 02 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.7-0.rc2.1mdk
- rc2.
- bk3.

* Tue May 25 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.7-0.rc1.1mdk
- rc1.
- bootsplash 3.1.5 20040318.
- netfilter (CLASSIFY CONNMARK IPMARK TARPIT addrtype condition connbytes
  h323-conntrack-nat owner-socketlookup pptp-conntrack-nat connlimit
  dstlimit iprange mport nth osf quota random time rtsp-conntrack)

* Wed May 19 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.6-3mdk
- bk6.
- kexec (do reboot,shutdown -r obselete ;)).
- ramdisk BIG fixes.
- quirks disable usb smm bios only on X86 (svetljo).
- drop kdb.

* Fri May 14 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.6-2mdk
- raid locking fix.
- r8169 266-mm2 updates.
- nfs long symlinks fix.
- atkbd_interrupt-interaction.
- input tsdev fixes.
- scancode keycode conversion for 265 fix.
- unplug can sleep.
- sata speedup.
- logitech keyboard fix.
- shm do munmap check.
- set_page_dirty nobuffers race fix.
- revert i8042 interrupt handling.
- fealnx fixes.
- kgdb support.
- acpi procfs fix.
- shfs 0.33.
- isdn devfs support.

* Fri May 10 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.6-1mdk
- 2.6.6.
- DI01 is back, not merged in upstream 
  (ide generic no via8237 sata basic support)

* Fri May  7 2004 Thomas Backlund <tmb@mandrake.org> 2.6.6-0.rc3.1mdk
- 2.6.6-rc3
- rediffed CK01-5
- drop DI01, ZY60 (merged upstream)
- drop MC06 (3rdparty prism54, merged upstream)
- add DV35: add missing errno to tda1004x
- update configs (new stuff in rc3):
  * CONFIG_ATM_FORE200E_USE_TASKLET=y
  * CONFIG_SECURITY_SELINUX_DISABLE=y

* Fri Apr 23 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.6-0.rc2.1mdk
- 2.6.6-rc2.
- lirc devfs remove fix.
- ia64 support.
- eagle-usb 1.9.6.

* Mon Apr 19 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.3-10mdk
- acpi cardbus pci routing fix.
- yenta irq routing fix for TI chipset.
- oss cmpci driver update to 6.64. 
- BIG isdn update.
- set max symlink to 10.
- gzloop (pixel).
- changeloop (pixel).
- vfat nobadchars option.
- supermount no warning when busy.
- sk98lin buggy vpd workaround. (bad eeprom on ASUS K8V)
- psmouse usb quirks fix (svetljo).
- CAN-2004-0003 r128.
- CAN-2004-0075 vicam.
- CAN-2004-0109 isofs fix.
- CAN-2004-0177 ext3.

* Fri Apr 16 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.3-9mdk
- Merge from AMD64 branch:
  * smaller -BOOT kernel
  * really add /proc/BOOT/{vbe,edid} interfaces
  * update K8 PowerNow!
  * update AMD64 subsystem to selected bits from 2.6.5rc2-1 patchkit
  * workaround VIA IOMMU problems
  * assorted libata fixes (SuSE)
  * enable mga drm & fix 32-bit drm thunks
  * support ITE it8212 RAID chip (Svetljo)
  * update libata core to 2004/03/09 (libata 1.01, sata_promise 0.91)

* Fri Apr 02 2004 Stew Benedict <nplanel@mandrakesoft.com> 2.6.3-8mdk
- CAN-2004-0109 isofs rockridge issue (ZY58)
- CAN-2004-0133 xfs filesystem issue (ZY59)
- CAN-2004-0177 ext3/jbd filesystem issue (ZY60)
- CAN-2004-0178 sb_audio issue (ZY61)
- CAN-2004-0181 jfs filesystem issue (ZY62)

* Wed Mar 17 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.3-7mdk
- revert xfs updates
- x86_64 really disable IO-APIC on NVIDIA boards (gb)
- usblp updates.
- sys_alarm return value fix.
- edd get legacy parameters.
- fbcon switch fix.
- ide-scsi error handling fixes.
- tun name fix.
- ehci use dma mapping.
- scsi alignment fix.

* Tue Mar  9 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.3-6mdk
- at76c503a 0.12 Beta8 with MSI6978 Wlan PC2PC support.
- lsb loop test must be work now.
- d_alloc_root, vma corruption, ramdisk memleak fixes.
- ext2/3 no space left fix.
- ICH6 update/fix ID.
- pdc202xx_old updates.
- loop setup race fix.
- pcnet32 transmit hang fix.
- e1000 5.2.30.1-k2.
- AMD 768MPX bootmem fix.
- floppy oops fix.
- i2o bugfixes.
- netfilter ip-route forget proto fix.
- cryptoloop support in BOOT kernel (pixel request).
- from tmb kernel:
  * remove qla2xxx from 3rdparty as it's already in main kernel.org
  * add support for mppe (svtljo)
  * pwc 9.0 Beta1.

* Thu Mar  4 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.6.3-5mdk
- add 32-bit DRM thunks for AMD64 (Egbert Eich).
- update AMD64 bits to 2.6.3-2 patchkit for ia32e support.

* Mon Mar 01 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.3-4mdk
- netfilter rtsp.
- dcache security fix.
- usb released wait on deregister bus.
- usb-storage update.
- ICH6 piix/libata support.
- aacraid update.
- sk98lin update.
- mtp fusion update to 3.00.03.
- ext3 fix access POSIX compiliant.
- pm runtime deadlock fix.

* Tue Feb 24 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.3-3mdk
- sg direct io allowed as default.
- bdclaim security oops fix.
- blacklist Compaq ProLiant DL360 (acpi=off).
- ipmi v30 (erwan request).

* Mon Feb 23 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.3-2mdk
- bootsplash working now.
- bootsplash compil depend fix (chmou).
- no more ide cdrom use ide-scsi.
- fix libata pci quirks (remove 0x24d1).
- parport updates.
- enable ATM in BOOT kernel (tv request).

* Fri Feb 20 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.3-1mdk
- acpi 20040211.
- nforce chipset must be working now.
- lirc create good /dev/lirc/0 now.
- alsa ac97, intel8x0, via82xx updates.
- remove udev requires.

* Thu Feb 12 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.2-3mdk
- ata_piix doesn't probe 8086:24d1 anymore for the moment.
- remove nforce bad patch.

* Wed Feb 11 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.2-2mdk
- acpi updates 20040211
- usb updates 20040211
- pnpbios=off as default.
- smb3 uid/gid permisions security fix.
- nforce irq setup fix.
- md update from mm.
- remove airo_mpi and mpi350, merged in airo module kernel.
- parallel port SCSI adapter (ppSCSI) support.
- prism54 20040210.
- hostap 0.1.3.
- at76c503 0.12Beta4.

* Thu Feb 05 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.2-1mdk
- 2.6.2 enjoy ;)
- qla2xxx updates.
- acx100 0.2.0pre7.
- alsa 1.0.2c.
- bttv, saa7134, cx88 updates.
- logitech wheel mouse must be work now.
- usb, input bk updates.
- alsa usx2y nforce3 pdplus PDAudio echoaudio drivers (tmb).

* Mon Feb 02 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.2-0.rc3.1mdk
- 2.6.2-rc3
- pnp updates.
- aureal sound cards support. (tmb)
- nForce2 apic fixies. (tmb)
- reeanble lirc. (not lirc_mceusb)

* Fri Jan 30 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.2-0.rc2.2mdk
- amd64 support (gb)
- new wireless drivers : poldhu, mpi350
- drm updates
- reiserfs in non-debug mode

* Mon Jan 26 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.2-0.rc2.1mdk
- 2.6.2-rc2.
- acpi 20040116.
- somes mm3 patches.
- alsa 1.0.2 (true verison)
- 80x25 mode selected if vesa mode is bad.
- usb gadget updates from David Brownell.
- dmi updates, pnpbios broken on Intel D865GBF and ASUS A7V8X.
- s/adiusbadsl/eagle-usb/ (new version)
- no module rename (s/[-,]/_/) pixel is a happiest man now ;)
- sync 3rd modules from tmb kernel.

* Wed Jan 21 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.2-0.rc1.1mdk
- 2.6.2. rc1
- agpgart as module now.
- remove drm cvs updates.

* Fri Jan 16 2004 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.1-1mdk
- 2.6.1. bk4
- force inline memcmp when use Os (gb)
- slim BOOT kernel.
- forcedeth v20.
- ndis wrapper 0.4.
- alsa 1.0.1.
- acpi 20031203.
- raid6 20040107.
- drm 20040108.
- nfs/nfsd updates.

* Thu Dec 18 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-1mdk
- 2.6.0 final version ;)
- ndis wrapper 0.3.
- fix uss725.

* Wed Dec 17 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.5mdk
- bk13.
- acecad 1.3.
- uss725.
- bttv videodev i2c videobuf updates 20031216.
- dvb timeout fix.
- mod_marvel (Kevin O'Connor).
- matrox_fb fixes (Kevin O'Connor).
- forcedeth v19.
- kdb build fix.
- add siimage 3114 support.
- prism25 0.2.1-pre16.
- qc-usb cvs20031216.

* Fri Dec 12 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.4mdk
- bk8.
- add vt|ar5k wireless chipset support.
- dos partition table consistency.
- warly touch boot logo ;)
- ndis wrapper 0.2. (only for up kernel)
- alsa 1.0.0rc2.
- agpgart and mousedev as built-in.

* Thu Dec 04 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.3mdk
- bk1:
  * ide-scsi.c uninitialized variable
  * x86 kernel page fault error codes
  * lost wakeups problem
  * missing initialization of /proc/net/tcp seq_file
- rework merge version.h (now all kernel have UTS_RELEASE defined)
- 2.6.0-test11q2 :
  * libata update
  * pwc 8.12
  * prism54 cvs20031203
  * alsa 1.0.0rc1

* Fri Nov 28 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.2mdk
- re-support on the fly module building (great for properitary packages)
- 2.6.0-test11q2 :
  * lots of mm patches
  * import somes 3rdparty and patches : (svetoslav)
    * lirc
    * at76c503a
    * bcm5700
    * dfg1394
    * dxr3
    * iscsi-mod
    * lufs
    * ov511
    * prism25
    * prism54
    * qc-usb

* Mon Nov 24 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.1mdk
- First version to move on kernel-2.6.0. (aka: ready for a new age).
- 2.6.0-test10q1 :
  * only i386 config for the moment
  * bootsplash 3.1.3
  * mdk logo
  * forcedeth v18
  * adiusbadsl 1.0.4 (untested)
  * acx100 0.2.0pre6
  * hostap 0.1.2

# Local Variables:
# rpm-spec-insert-changelog-version-with-shell: t
# End:
