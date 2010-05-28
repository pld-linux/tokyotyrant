Summary:	Network interface for the Tokyo Cabinet database
Summary(pl.UTF-8):	Interfejs sieciowy dla bazy danych Tokyo Cabinet
Name:		tokyotyrant
Version:	1.1.40
Release:	0.4
License:	LGPL
Group:		Libraries
Source0:	http://1978th.net/tokyotyrant/%{name}-%{version}.tar.gz
# Source0-md5:	cc9b7f0c6764d37700ab43d29a5c6048
Source1:	%{name}.init
Source2:	%{name}-example-config
URL:		http://1978th.net/tokyotyrant/
BuildRequires:	tokyocabinet-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/sbin/groupadd
Requires:	rc-scripts >= 0.4.1.23
Provides:	group(tokyotyrant)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tokyo Tyrant is a network interface daemon and client library for the
Tokyo Cabinet database, intended for concurrent and/or remote access
to a database file.

%description -l pl.UTF-8
Tokyo Tyrant to interfejs sieciowy - demon oraz biblioteka kliencka -
dla bazy danych Tokyo Cabinet, służący do zapewnienia równoległego
i/lub zdalnego dostępu do pliku bazy danych.

%package devel
Summary:	Header files for tokyotyrant client library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki klienckiej tokyoryrant
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for tokyotyrant client library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki klienckiej tokyotyrant.

%package libs
Summary:	Tokyotyrant client library
Summary(pl.UTF-8):	Biblioteka kliencka tokyotyrant
Group:		Development/Libraries

%description libs
Tokyotyrant client library.

%description libs -l pl.UTF-8
Biblioteka kliencka tokyotyrant.

%package static
Summary:	Static tokyotyrant client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka tokyotyrant
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static tokyotyrant client library.

%description static -l pl.UTF-8
Statyczna biblioteka kliencka tokyotyrant.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{tokyotyrant.d,rc.d/init.d}
install -d $RPM_BUILD_ROOT/var/run/tokyotyrant

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Remove the provided init script, it is useless. SOURCE1 replaces it.
rm -f $RPM_BUILD_ROOT%{_sbindir}/ttservctl

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/tokyotyrant.d/example

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 252 %{name}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%groupremove %{name}
fi

%post libs	-p /sbin/ldconfig
%postun libs	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/tt*.so
%dir %attr(751,root,root) %{_sysconfdir}/tokyotyrant.d
%{_sysconfdir}/tokyotyrant.d/example
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*
%dir %attr(770,root,tokyotyrant) /var/run/tokyotyrant

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtokyotyrant.so
%{_includedir}/t*.h
%{_pkgconfigdir}/*.pc
%{_mandir}/man3/*.3*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libtokyotyrant.so.3
%attr(755,root,root) %{_libdir}/libtokyotyrant.so.*.*.*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtokyotyrant.a
