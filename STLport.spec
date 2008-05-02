# TODO
# - fix ppc build
Summary:	C++ standard library
Summary(pl.UTF-8):	Biblioteki standardowe C++
Name:		STLport
Version:	5.1.2
Release:	2
Epoch:		2
License:	distributable (see README.gz)
Group:		Libraries
Source0:	http://dl.sourceforge.net/stlport/%{name}-%{version}.tar.bz2
# Source0-md5:	937b114455f304eb1cf7b9cc2ca103a3
Patch0:		%{name}-endianness.patch
Patch1:		%{name}-gcc420_dirty_hack.patch
Patch2:		%{name}-no_vendor_math_l.patch
Patch3:		%{name}-alpha.patch
URL:		http://stlport.sourceforge.net/
BuildRequires:	libstdc++-devel >= 5:3.3.2
BuildRequires:	sed >= 4.0
%requires_eq	libstdc++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
STLport is a multiplatform implementation of C++ Standard Template
Library based on SGI STL. It's used by e.g. OpenOffice.

%description -l pl.UTF-8
STLport to wieloplatformowa implementacja standardowej biblioteki
szablonów (Standard Template Library) C++ oparta na SGI STL. Jest
używana m.in. przez OpenOffice.

%package devel
Summary:	STLport heades files, documentation
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do STLport
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for STLport.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja dla STLport.

%package static
Summary:	Static STLport libraries
Summary(pl.UTF-8):	Biblioteki statyczne do STLport
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static STLport libraries.

%description static -l pl.UTF-8
Biblioteki statyczne do STLport.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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

# libstlport.so.5 is removed by ldconfig or *something*, so make .so point to real soname
ln -sf $(cd $RPM_BUILD_ROOT%{_libdir}; echo libstlport.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libstlport.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libstlport.so.*.*
# libstlport.so points to this one instead of soname or real lib name
# to be fixed if nothing tries to dlopen this one (nothing should!)
%attr(755,root,root) %{_libdir}/libstlport.so.?

%files devel
%defattr(644,root,root,755)
%doc doc/{FAQ,*.txt}
%attr(755,root,root) %{_libdir}/libstlport.so
%{_includedir}/stlport

%files static
%defattr(644,root,root,755)
%{_libdir}/libstlport.a
