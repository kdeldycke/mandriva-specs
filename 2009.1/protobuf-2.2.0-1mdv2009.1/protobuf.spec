%define name    protobuf
%define version 2.2.0
%define release %mkrel 1

# don't build -python subpackage
%define with_python   %{?_without_python: 0} %{?!_without_python: 1}
# don't build -java subpackages
# -- -- %define with_java     %{?_without_java:   0} %{?!_without_java:   1}
%define with_java 0
# don't require gtest for building
%define without_gtest %{?_without_gtest:  1} %{?!_without_gtest:  0}
%define without_gtest 1


Summary:        Protocol Buffers - Google's data interchange format
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        BSD
Group:          Development/Libraries
Source:         http://protobuf.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:        ftdetect-proto.vim
URL:            http://code.google.com/p/protobuf/
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  automake autoconf libtool pkgconfig
%if !%{without_gtest}
BuildRequires:  gtest-devel
%endif

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package lite
Summary: Protocol Buffers lite version
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description lite
This package contains a light version of Google's Protocol Buffers library

%package compiler
Summary: Protocol Buffers compiler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-lite = %{version}-%{release}

%description compiler
This package contains Protocol Buffers compiler for all programming
languages

%package devel
Summary: Protocol Buffers C++ headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-lite = %{version}-%{release}
Requires: %{name}-compiler = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package static
Summary: Static development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-lite = %{version}-%{release}

%description static
Static libraries for Protocol Buffers

%if %{with_python}
%package python
Summary: Python bindings for Google Protocol Buffers
Group: Development/Languages
BuildRequires: libpython-devel
BuildRequires: python-setuptools
Conflicts: %{name}-compiler > %{version}
Conflicts: %{name}-compiler < %{version}

%description python
This package contains Python libraries for Google Protocol Buffers
%endif

%package vim
Summary: Vim syntax highlighting for Google Protocol Buffers descriptions
Group: Development/Libraries
Requires: vim-enhanced

%description vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor

%if %{with_java}
%package java
Summary: Java Protocol Buffers runtime library
Group:   Development/Languages
BuildRequires:    java-devel >= 1.6
BuildRequires:    jpackage-utils
BuildRequires:    maven2
BuildRequires:    maven2-plugin-compiler
BuildRequires:    maven2-plugin-install
BuildRequires:    maven2-plugin-jar
BuildRequires:    maven2-plugin-javadoc
BuildRequires:    maven2-plugin-release
BuildRequires:    maven2-plugin-resources
BuildRequires:    maven2-plugin-surefire
BuildRequires:    maven2-plugin-antrun
Requires:         java
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils
Conflicts:        %{name}-compiler > %{version}
Conflicts:        %{name}-compiler < %{version}

%description java
This package contains Java Protocol Buffers runtime library.

%package javadoc
Summary: Javadocs for %{name}-java
Group:   Documentation
Requires: jpackage-utils
Requires: %{name}-java = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}-java.

%endif

%prep
%setup -q
chmod 644 examples/*

%build
export PTHREAD_CFLAGS="-lpthread"
./autogen.sh
%configure
%make %{?_smp_mflags}

%if %{with_python}
pushd python
python ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd
%endif

%if %{with_java}
pushd java
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-jpp -Dmaven.repo.local=$MAVEN_REPO_LOCAL install javadoc:javadoc
popd
%endif

%check
%make %{?_smp_mflags} check

%install
%{__rm} -rf %{buildroot}
%makeinstall
find %{buildroot} -type f -name "*.la" -exec rm -f {} \;
%if %{with_python}
pushd python
python ./setup.py install --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd
%endif
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with_java}
pushd java
install -d -m 755 %{buildroot}%{_javadir}
install -pm 644 target/%{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}

install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap org.apache.maven %{name} %{version} JPP %{name}

%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post lite -p /sbin/ldconfig
%postun lite -p /sbin/ldconfig

%post compiler -p /sbin/ldconfig
%postun compiler -p /sbin/ldconfig

%if %{with_java}
%post java
%update_maven_depmap

%postun java
%update_maven_depmap
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_libdir}/libprotobuf.so.*
%doc CHANGES.txt CONTRIBUTORS.txt COPYING.txt README.txt

%files lite
%defattr(-, root, root, -)
%{_libdir}/libprotobuf-lite.so.*
%doc COPYING.txt README.txt

%files compiler
%defattr(-, root, root, -)
%{_bindir}/protoc
%{_libdir}/libprotoc.so.*
%doc COPYING.txt README.txt

%files devel
%defattr(-, root, root, -)
%dir %{_includedir}/google
%{_includedir}/google/protobuf/
%{_libdir}/libprotobuf.so
%{_libdir}/libprotobuf-lite.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc
%{_libdir}/pkgconfig/protobuf-lite.pc
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.txt

%files static
%defattr(-, root, root, -)
%{_libdir}/libprotobuf.a
%{_libdir}/libprotobuf-lite.a
%{_libdir}/libprotoc.a
%if %{with_python}
%files python
%defattr(-, root, root, -)
%dir %{python_sitelib}/google
%{python_sitelib}/google/protobuf/
%{python_sitelib}/protobuf-%{version}-py%{python_version}.egg-info/
%{python_sitelib}/protobuf-%{version}-py%{python_version}-nspkg.pth
%doc python/README.txt
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%endif

%files vim
%defattr(-, root, root, -)
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with_java}
%files java
%defattr(-, root, root, -)
%{_datadir}/maven2/poms/JPP-protobuf.pom
%{_mavendepmapfragdir}/protobuf
%{_javadir}/*
%doc examples/AddPerson.java examples/ListPeople.java

%files javadoc
%defattr(-, root, root, -)
%{_javadocdir}/%{name}
%endif

%changelog
* Tue Aug 18 2009 Kevin Deldycke <kevin@deldycke.com> 2.2.0-1mdv2009.1
- Upgrade to protobuf 2.2.0
- Add -lpthread option to environment (else configure set it to -pthread)
- Use strandard mandriva RPM macros to build the package
- Remove all patches 
- Remove pkg-config stuff (now part of protobuf since commit #177: http://code.google.com/p/protobuf/source/detail?r=177 )
- Add lite package flavour
- No need to redefine python_sitelib variable, it already set to the right value by Mandriva's RPM macros
- Generate automaticcaly names of python files to include in the package

* Fri May 29 2009 Kevin Deldycke <kevin@deldycke.com> 2.0.2-1mdv2009.1
- Backported from Fedora Core 11 to Mandriva 2009.1 (source: ftp://ftp.icm.edu.pl/vol/rzm1/linux-fedora-secondary/development/source/SRPMS/protobuf-2.0.2-6.fc11.src.rpm )
- Force build without gtest
- Adapt python dependencies to fit Mandriva's

* Tue Dec 23 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-6
- Small fixes for python 2.6 eggs.
- Temporarily disabled java subpackage due to build problems, will be fixed and
  turned back on in future.

* Thu Nov 27 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-5
- No problems with ppc & ppc64 arch in rawhide, had to do a release bump.

* Sat Nov 22 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-4
- Added patch from subversion r70 to workaround gcc 4.3.0 bug (see
  http://code.google.com/p/protobuf/issues/detail?id=45 for more
  details).

* Tue Nov 11 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-3
- Added conflicts to java and python subpackages to prevent using with
  wrong compiler versions.
- Fixed license.
- Fixed BuildRequires for -python subpackage.
- Fixed Requires and Group for -javadoc subpackage.
- Fixed Requires for -devel subpackage.
- Fixed issue with wrong shebang in descriptor_pb2.py.
- Specify build options via --with/--without.
- Use Fedora-packaged gtest library instead of a bundled one by
  default (optional).

* Fri Oct 31 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-2
- Use python_sitelib macro instead of INSTALLED_FILES.
- Fix the license.
- Fix redundant requirement for -devel subpackage.
- Fix wrong dependences for -python subpackage.
- Fix typo in requirements for -javadoc subpackage.
- Use -p option for cp and install to preserve timestamps.
- Remove unneeded ldconfig call for post scripts of -devel subpackage.
- Fix directories ownership.

* Sun Oct 12 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-1
- Update to version 2.0.2
- New -java and -javadoc subpackages.
- Options to disable building of -python and -java* subpackages

* Mon Sep 15 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.1-2
- Added -p switch to install commands to preserve timestamps.
- Fixed Version and Libs in pkgconfig script.
- Added pkgconfig requires for -devel package.
- Removed libtool archives from -devel package.

* Thu Sep 04 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.1-1
- Updated to 2.0.1 version.

* Wed Aug 13 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.0-0.1.beta
- Initial package version. Credits for vim subpackage and pkgconfig go
  to Rick L Vinyard Jr <rvinyard@cs.nmsu.edu>
