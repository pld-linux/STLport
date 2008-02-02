Summary:	C++ standard library
Summary(pl.UTF-8):	Biblioteki standardowe C++
Name:		STLport
Version:	5.1.5
Release:	1
Epoch:		2
License:	distributable (see README.gz)
Group:		Libraries
Source0:	http://dl.sourceforge.net/stlport/%{name}-%{version}.tar.bz2
# Source0-md5:	e31d0dc9141c4f264d887754b559cc84
Patch0:		%{name}-endianness.patch
Patch1:		%{name}-alpha.patch
Patch2:		%{name}-valarray-copy-constructor.patch
URL:		http://stlport.sourceforge.net/
BuildRequires:	libstdc++-devel >= 6:4.2.0-1
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

%package dbg
Summary:	Debug version of STLport library
Summary(pl.UTF-8):	Wersja diagnostyczna biblioteki STLport
Group:		Libraries
%requires_eq	libstdc++

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
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i -e 's/= -O2$/= %{rpmcflags}/' build/Makefiles/gmake/gcc.mak

%build
%{__make} -C build/lib -f gcc.mak \
	stldbg-shared \
	stldbg-static \
	release-shared \
	release-static \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

%{__make} -C build/lib -f gcc.mak \
	install-stldbg-shared \
	install-stldbg-static \
	install-release-shared \
	install-release-static \
	INSTALL_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_LIB_DIR_STLDBG=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_LIB_DIR=$RPM_BUILD_ROOT%{_libdir}

cp -a stlport $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_includedir}/stlport/BC50

# let libstlport{,stlg}.so point to real lib, not artificial libstlport{,stlg}.so.5 symlink
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libstlport.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libstlport.so
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libstlportstlg.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libstlportstlg.so

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
%attr(755,root,root) %ghost %{_libdir}/libstlport.so.5.1

%files devel
%defattr(644,root,root,755)
%doc doc/{FAQ,*.txt}
%attr(755,root,root) %{_libdir}/libstlport.so
%{_includedir}/stlport

%files static
%defattr(644,root,root,755)
%{_libdir}/libstlport.a

%files dbg
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstlportstlg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstlportstlg.so.5.1

%files dbg-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstlportstlg.so

%files dbg-static
%defattr(644,root,root,755)
%{_libdir}/libstlportstlg.a
