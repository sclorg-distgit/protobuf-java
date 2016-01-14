%{?scl:%scl_package protobuf-java}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

# Exclude generation of osgi() style provides, since they are not
# SCL-namespaced and may conflict with base RHEL packages.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1045449
%global __provides_exclude ^osgi(.*)$

Name:           %{?scl_prefix}protobuf-java
Version:        2.5.0
Release:        10%{?dist}
License:        BSD
Summary:        Java Protocol Buffers runtime library
Group:          Development/Languages
Source:         http://protobuf.googlecode.com/files/protobuf-%{version}.tar.bz2
Patch2:         protobuf-2.5.0-java-fixes.patch
URL:            http://code.google.com/p/protobuf/

BuildRequires:    %{?scl_prefix_java_common}maven-local
BuildRequires:    %{?scl_prefix_maven}maven-compiler-plugin
BuildRequires:    %{?scl_prefix_maven}maven-install-plugin
BuildRequires:    %{?scl_prefix_maven}maven-jar-plugin
BuildRequires:    %{?scl_prefix_maven}maven-javadoc-plugin
BuildRequires:    %{?scl_prefix_maven}maven-resources-plugin
BuildRequires:    %{?scl_prefix_maven}maven-surefire-plugin
BuildRequires:    %{?scl_prefix_maven}maven-antrun-plugin
BuildRequires:    autoconf automake libtool pkgconfig zlib-devel
Requires:         java
%{?scl:Requires: %scl_runtime}

%description
This package contains Java Protocol Buffers runtime library.

%package javadoc
Summary: Javadocs for %{name}
Group:   Documentation
%{?scl:Requires: %scl_runtime}

%description javadoc
This package contains the API documentation for %{name}-java.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n protobuf-%{version}
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
./autogen.sh
%configure
%patch2 -p1 -b .java-fixes
%{?scl:EOF}

%build
make

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
pushd java
%mvn_build -f
popd
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
pushd java
%mvn_install
popd
# Own the protobuf-java directory in order to avoid it sticking
# around after removal
install -d -m 755 %{buildroot}%{_javadir}/%{name}
%{?scl:EOF}

%files -f java/.mfiles
# Own directory where xmvn installs in.
%dir %{_javadir}/%{name}

%files javadoc -f java/.mfiles-javadoc

%changelog
* Mon Jan 16 2015 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-10
- Switch to rh-java-common's maven-local as BR.

* Tue Jan 13 2015 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-9
- Rebuild for properly generated provides/requires.

* Fri Dec 19 2014 Severin Gehwolf <sgehwolf@redhat.com> 2.5.0-8
- Use maven30 collection for building.
- Use java common's requires/provides generators.

* Mon Jun 23 2014 Severin Gehwolf <sgehwolf@redhat.com> 2.5.0-7
- Add requires for thermostat1-runtime package.
- Filter osgi()-style provides.
- Own scl-ized directory.

* Wed Nov 27 2013 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-6
- Properly enable SCL.

* Tue Nov 12 2013 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-5
- Initial SCL-ized package.
