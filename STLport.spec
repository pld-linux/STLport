Summary:	C++ standard library
Summary(pl):	Biblioteki standardowe C++ 
Name:		STLport
Version:	4.5.3
Release:	3
License:	distributable (see README.gz)
Group:		Libraries
Source0:	http://www.stlport.com/archive/%{name}-%{version}.tar.gz
Patch0:		%{name}-nodebug.patch
Patch1:		%{name}-gcc3.patch
Patch2:		%{name}-4.5.3-gcc3stdexcept.patch
Patch3:		%{name}-4.5.3-nobadlink.patch
Patch4:		%{name}-4.5.3-extra-cxxflags.patch
URL:		http://www.stlport.org/
BuildRequires:	gcc-c++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of C++ standard library required by OpenOffice.

%description -l pl
Implementacja standardowej biblioteki C++ wymaganej przez OpenOffice.

%package devel
Summary:	STLport heades files, documentation
Summary(pl):	Pliki nag³ówkowe i dokumentacja do STLport
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for STLport.

%description -l pl devel
Pliki nag³ówkowe i dokumentacja dla STLport.

%package static
Summary:	Static STLport libraries
Summary(pl):	Biblioteki statyczne do STLport
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static STLport libraries.

%description -l pl static
Biblioteki statyczne do STLport.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1

%build
cd src
CXXFLAGS="%{rpmcflags}" \
%{__make} -f gcc.mak 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}

rm -fr stlport/{BC50,old_hp}
cp -fr stlport $RPM_BUILD_ROOT%{_includedir}
install lib/*.a $RPM_BUILD_ROOT%{_libdir}
install lib/*.so.* $RPM_BUILD_ROOT%{_libdir}
ln -sf libstlport_gcc.so.4.5 $RPM_BUILD_ROOT%{_libdir}/libstlport_gcc.so

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/* README
%{_includedir}/stlport
%{_libdir}/*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
