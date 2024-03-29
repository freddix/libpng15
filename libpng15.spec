Summary:	PNG library
Name:		libpng15
Version:	1.5.17
Release:	1
Epoch:		2
License:	distributable
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libpng/libpng-%{version}.tar.xz
# Source0-md5:	6509aba334bbd87613d2d353a2af44d6
Patch0:		libpng-pngminus.patch
# https://sourceforge.net/projects/apng/files/libpng/
Patch1:		http://downloads.sourceforge.net/libpng-apng/libpng-%{version}-apng.patch.gz
URL:		http://www.libpng.org/pub/png/libpng.html
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The PNG library is a collection of routines used to create and
manipulate PNG format graphics files. The PNG format was designed as a
replacement for GIF, with many improvements and extensions.

%package devel
Summary:	Header files for libpng
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
The header files are only needed for development of programs using the
PNG library.

%package static
Summary:	Static png library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static ppng library.

%package progs
Summary:	libpng utility programs
Group:		Applications/Graphics
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description progs
This package contains utility programs to convert PNG files to and
from PNM files.

%prep
%setup -qn libpng-%{version}
%patch0 -p1
%patch1 -p1

%build
%if 0
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%endif
%configure
%{__make}
%{__make} -C contrib/pngminus -f makefile.std	\
	CC="%{__cc}"				\
	LIBPATH=%{_libdir}			\
	OPT_FLAGS="%{rpmcppflags} %{rpmcflags}"	\
	PNGLIB="-L../../.libs -lpng15"

%check
%{__make} -j1 check

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install contrib/pngminus/{png2pnm,pnm2png} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE CHANGES README LICENSE
%attr(755,root,root) %ghost %{_libdir}/libpng15.so.??
%attr(755,root,root) %{_libdir}/libpng15.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc *.txt
%attr(755,root,root) %{_bindir}/libpng*-config
%attr(755,root,root) %{_libdir}/libpng*.so
%{_includedir}/libpng15
%{_includedir}/png*.h
%{_pkgconfigdir}/libpng*.pc

%{_mandir}/man3/libpng.3*
%{_mandir}/man3/libpngpf.3*
%{_mandir}/man5/png.5*

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpng*.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/png2pnm
%attr(755,root,root) %{_bindir}/pnm2png

