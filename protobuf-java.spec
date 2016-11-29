%{?scl:%scl_package protobuf-java}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

%if 0%{?rhel}

%if 0%{?rhel} <= 6
  # EL 6
  %global custom_release 60
%else
  # EL 7
  %global custom_release 70
%endif

%else

%global custom_release 1

%endif

# there is no native code so a debuginfo package is
# bound to be empty: do not produce the empty package
%global debug_package %{nil}

Name:           %{?scl_prefix}protobuf-java
Version:        2.5.0
Release:        %{custom_release}.2%{?dist}
License:        BSD
Summary:        Java Protocol Buffers runtime library
Group:          Development/Languages
Source:         http://protobuf.googlecode.com/files/protobuf-%{version}.tar.bz2
Patch2:         protobuf-2.5.0-java-fixes.patch
URL:            http://code.google.com/p/protobuf/

BuildRequires:    %{?scl_prefix_maven}maven-local
BuildRequires:    %{?scl_prefix_maven}maven-compiler-plugin
BuildRequires:    %{?scl_prefix_maven}maven-install-plugin
BuildRequires:    %{?scl_prefix_maven}maven-jar-plugin
BuildRequires:    %{?scl_prefix_maven}maven-javadoc-plugin
BuildRequires:    %{?scl_prefix_maven}maven-resources-plugin
BuildRequires:    %{?scl_prefix_maven}maven-surefire-plugin
BuildRequires:    %{?scl_prefix_maven}maven-antrun-plugin
BuildRequires:    autoconf automake libtool pkgconfig zlib-devel

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
# Own the protobuf-java directory in order to avoid it sticking
# around after removal
install -d -m 755 %{buildroot}%{_javadir}/%{pkg_name}
%{?scl:EOF}

%files -f java/.mfiles
# Own directory where xmvn installs in.
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f java/.mfiles-javadoc

%changelog
* Tue Jul 26 2016 Jie Kang <jkang@redhat.com> - 2.5.0-2
- Do not produce empty debuginfo package

* Thu Jun 23 2016 Severin Gehwolf <sgehwolf@redhat.com> - 2.5.0-1
- Initial package.
