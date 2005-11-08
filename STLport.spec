Summary:	C++ standard library
Summary(pl):	Biblioteki standardowe C++
Name:		STLport
Version:	5.0.0
Release:	0.1
Epoch:		2
License:	distributable (see README.gz)
Group:		Libraries
Source0:	http://www.stlport.com/archive/%{name}-%{version}.tar.bz2
# Source0-md5:	5aefcbb0c30a91d50bb2d6c7b30e8393
Patch0:		%{name}-nodebug.patch
Patch1:		%{name}-soname.patch
Patch2:		%{name}-gcc34.patch
Patch3:		%{name}-4.5.3-gcc3stdexcept.patch
Patch4:		%{name}-4.5.3-extra-cxxflags.patch
URL:		http://www.stlport.org/
BuildRequires:	libstdc++-devel >= 5:3.3.2
%requires_eq	libstdc++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
STLport is a multiplatform implementation of C++ Standard Template
Library based on SGI STL. It's used by e.g. OpenOffice.

%description -l pl
STLport to wieloplatformowa implementacja standardowej biblioteki
szablon�w (Standard Template Library) C++ oparta na SGI STL. Jest
u�ywana m.in. przez OpenOffice.

%package devel
Summary:	STLport heades files, documentation
Summary(pl):	Pliki nag��wkowe i dokumentacja do STLport
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for STLport.

%description devel -l pl
Pliki nag��wkowe i dokumentacja dla STLport.

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
#patch0 -p1
#patch1 -p1
#patch2 -p1
#patch3 -p1
#patch4 -p1

%build
%{__make} -C build/lib -f gcc.mak \
	release-shared \
	release-static \
	CXXFLAGS="%{rpmcxxflags}" \
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
%attr(755,root,root) %{_libdir}/*.so.*.*
%attr(755,root,root) %{_libdir}/*.so

%files devel
%defattr(644,root,root,755)
%doc doc/{FAQ,*.txt}
%{_includedir}/stlport

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
