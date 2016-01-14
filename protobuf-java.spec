# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

%{?scl:%scl_package protobuf-java}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}protobuf-java
Version:        2.5.0
Release:        12%{?dist}
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

%description
This package contains Java Protocol Buffers runtime library.

%package javadoc
Summary: Javadocs for %{name}
Group:   Documentation

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
%{?scl:EOF}

%files -f java/.mfiles

%files javadoc -f java/.mfiles-javadoc

%changelog
* Tue Jan 20 2015 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-12
- Use java common's maven-local as BR.
- Use java common's requires/provides generators.

* Wed Dec 17 2014 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-11
- Don't hard-code maven collection name.

* Wed Jun 18 2014 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-10
- Build using maven30 collection.

* Tue Jan 21 2014 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-9
- Rebuild in order to fix build root which had broken
  jpackages-tools provides. See RHBZ#1042912.
- Related: RHBZ#1054813

* Wed Nov 27 2013 Elliott Baron <ebaron@redhat.com> - 2.5.0-8
- Properly enable SCL.

* Fri Nov 15 2013 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-7
- Add macro for java auto-requires/provides.

* Fri Nov 15 2013 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-6
- BR javapackages-tools.

* Tue Nov 12 2013 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-5
- Initial SCL-ized package.
