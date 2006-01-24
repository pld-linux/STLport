Summary:	C++ standard library
Summary(pl):	Biblioteki standardowe C++
Name:		STLport
Version:	5.0.1
Release:	0.1
Epoch:		2
License:	distributable (see README.gz)
Group:		Libraries
Source0:	http://dl.sourceforge.net/stlport/%{name}-%{version}.tar.bz2
# Source0-md5:	461cc1b11322568d75e3c0a4a1944cd1
Patch0:		%{name}-endianness.patch
URL:		http://stlport.sourceforge.net/
BuildRequires:	libstdc++-devel >= 5:3.3.2
BuildRequires:	sed >= 4.0
%requires_eq	libstdc++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
STLport is a multiplatform implementation of C++ Standard Template
Library based on SGI STL. It's used by e.g. OpenOffice.

%description -l pl
STLport to wieloplatformowa implementacja standardowej biblioteki
szablonów (Standard Template Library) C++ oparta na SGI STL. Jest
u¿ywana m.in. przez OpenOffice.

%package devel
Summary:	STLport heades files, documentation
Summary(pl):	Pliki nag³ówkowe i dokumentacja do STLport
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for STLport.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja dla STLport.

%package static
Summary:	Static STLport libraries
Summary(pl):	Biblioteki statyczne do STLport
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static STLport libraries.

%description static -l pl
Biblioteki statyczne do STLport.

%prep
%setup -q -n %{name}
%patch0 -p1

sed -i -e 's/= -O2$/= %{rpmcflags}/' build/Makefiles/gmake/gcc.mak

%build
%{__make} -C build/lib -f gcc.mak \
	release-shared \
	release-static \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

%{__make} -C build/lib -f gcc.mak \
	install-release-shared \
	install-release-static \
	INSTALL_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_LIB_DIR=$RPM_BUILD_ROOT%{_libdir}

cp -a stlport $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_includedir}/stlport/BC50

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%doc doc/{FAQ,*.txt}
%{_includedir}/stlport
%attr(755,root,root) %{_libdir}/*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
