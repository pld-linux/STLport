#
# Conditional build:
%bcond_with	static_gcc	# linkg libgcc* statically into libstlport.
#
Summary:	C++ standard library
Summary(pl.UTF-8):	Biblioteki standardowe C++
Name:		STLport
Version:	5.2.1
Release:	2
Epoch:		2
License:	distributable (see README.gz)
Group:		Libraries
Source0:	http://dl.sourceforge.net/stlport/%{name}-%{version}.tar.bz2
# Source0-md5:	a8341363e44d9d06a60e03215b38ddde
Source1:	stlport-config.in
Source2:	stlport.pc.in
Source3:	stlport-debug.pc.in
Patch0:		%{name}-endianness.patch
Patch1:		%{name}-alpha.patch
URL:		http://stlport.sourceforge.net/
BuildRequires:	libstdc++-devel >= 6:4.2.0-1
BuildRequires:	sed >= 4.0
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

%package dbg
Summary:	Debug version of STLport library
Summary(pl.UTF-8):	Wersja diagnostyczna biblioteki STLport
Group:		Libraries

%description dbg
Debug version of STLport library.

%description dbg -l pl.UTF-8
Wersja diagnostyczna biblioteki STLport.

%package dbg-devel
Summary:	Debug version of STLport library - development files
Summary(pl.UTF-8):	Wersja diagnostyczna biblioteki STLport - pliki programistyczne
Group:		Development/Libraries
Requires:	%{name}-dbg = %{epoch}:%{version}-%{release}
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description dbg-devel
Debug version of STLport library - development files.

%description dbg-devel -l pl.UTF-8
Wersja diagnostyczna biblioteki STLport - pliki programistyczne.

%package dbg-static
Summary:	Static debug version of STLport library
Summary(pl.UTF-8):	Statyczna wersja diagnostyczna biblioteki STLport
Group:		Development/Libraries
Requires:	%{name}-dbg-devel = %{epoch}:%{version}-%{release}

%description dbg-static
Static debug version of STLport library.

%description dbg-static -l pl.UTF-8
Statyczna wersja diagnostyczna biblioteki STLport.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

sed -i -e 's/= -O2$/= %{rpmcflags}/' build/Makefiles/gmake/gcc.mak

cp -a %{SOURCE1} stlport-config.in
cp -a %{SOURCE2} stlport.pc.in
cp -a %{SOURCE3} stlport-debug.pc.in

%build
./configure \
	--prefix=%{_prefix} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--with-cc=%{__cc} \
	--with-cxx=%{__cxx} \
	--without-debug \
	--enable-static \
	%{?with_static_gcc:--use-static-gcc} \
	--use-compiler-family=gcc

%{__make}

subst='
	s,@prefix@,%{_prefix},g
	s,@exec_prefix@,%{_exec_prefix},g
	s,@libdir@,%{_libdir},g
	s,@includedir@,%{_includedir},g
	s,@ver@,%{version},g
	s,@VERSION@,%{version},g
'

%{__sed} -e "$subst" stlport-config.in > stlport-config
%{__sed} -e "$subst" stlport.pc.in > stlport.pc
%{__sed} -e "$subst" stlport-debug.pc.in > stlport-debug.pc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_LIB_DIR_STLDBG=$RPM_BUILD_ROOT%{_libdir}

# let libstlport{,stlg}.so point to real lib, not artificial libstlport{,stlg}.so.5 symlink
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libstlport.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libstlport.so
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libstlportstlg.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libstlportstlg.so

install -d $RPM_BUILD_ROOT{%{_pkgconfigdir},%{_bindir}}
cp -a stlport.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
cp -a stlport-debug.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
install stlport-config $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	dbg -p /sbin/ldconfig
%postun dbg -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libstlport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstlport.so.5.2
%attr(755,root,root) %ghost %{_libdir}/libstlport.so.5

%files devel
%defattr(644,root,root,755)
%doc doc/{FAQ,*.txt}
%attr(755,root,root) %{_libdir}/libstlport.so
%attr(755,root,root) %{_bindir}/stlport-config
%{_includedir}/stlport
%{_pkgconfigdir}/stlport.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libstlport.a

%files dbg
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstlportstlg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstlportstlg.so.5.2
%attr(755,root,root) %ghost %{_libdir}/libstlportstlg.so.5

%files dbg-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstlportstlg.so
%{_pkgconfigdir}/stlport-debug.pc

%files dbg-static
%defattr(644,root,root,755)
%{_libdir}/libstlportstlg.a
