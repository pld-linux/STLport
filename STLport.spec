Summary:	C++ standard library
Summary(pl):	Biblioteki standardowe C++ 
Name:		STLport
Version:	4.0
Release:	3
License:	Propably OpenSource
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://www.stlport.com/archive/%{name}-%{version}.tar.gz
Patch0:		%{name}-nodebug.patch
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
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for STLport.

%description -l pl devel
Pliki nag³ówkowe i dokumentacja dla STLport.

%package static
Summary:	Static STLport libraries
Summary(pl):	Biblioteki statyczne do STLport
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static STLport libraries.

%description -l pl static
Biblioteki statyczne do STLport.

%prep
%setup -q
%patch0 -p1

%build
cd src
CXXFLAGS="%{rpmcflags}" \
%{__make} -f gcc.mak 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}

rm -fr stlport/{BC50,SC5,old_hp,wrap_std}
cp -fr stlport $RPM_BUILD_ROOT%{_includedir}
install lib/*.a $RPM_BUILD_ROOT%{_libdir}
install lib/*.so $RPM_BUILD_ROOT%{_libdir}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_includedir}/stlport

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
