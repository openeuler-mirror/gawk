%global gawk_api_major %(tar -xf %{name}-%{version}.tar.xz %{name}-%{version}/gawkapi.h --to-stdout |\
			 egrep -i "gawk_api_major.*[0-9]+" | egrep -o "[0-9]")
%global gawk_api_minor %(tar -xf %{name}-%{version}.tar.xz %{name}-%{version}/gawkapi.h --to-stdout |\
			 egrep -i "gawk_api_minor.*[0-9]+" | egrep -o "[0-9]")
Name:		gawk
Version:	5.0.1
Release:	1
License:	GPLv3+ and GPLv2+ and LGPLv2+ and BSD
Summary:	The GNU version of the AWK text processing utility
URL:		https://www.gnu.org/software/gawk/
Source0:	https://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.xz

BuildRequires:	git gcc automake grep
BuildRequires:	bison texinfo texinfo-tex ghostscript texlive-ec texlive-cm-super glibc-all-langpacks
BuildRequires:	libsigsegv-devel mpfr-devel readline-devel
Requires:	filesystem >= 3

Provides:	/bin/awk
Provides:	/bin/gawk
Provides:	gawk(abi) = %{gawk_api_major}.%{gawk_api_minor}

%description
The gawk package is the GNU implementation of awk.
The awk utility interprets a special-purpose programming language that
makes it possible to handle simple data-reformatting jobs with just a
few lines of code.

%package devel
Summary:          Header file for gawk extensions development
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description devel
This subpackage provides /usr/include/gawkapi.h header file, which contains
definitions for use by extension functions calling into gawk.

%package help
Summary:          Documentation for gawk utility
Requires:         %{name} = %{version}-%{release}
Requires:         man,info
BuildArch:        noarch
%description help
This subpackage provide addtional documents and manuals for gawk.

%package lang
Summary:        Language files and locale
Requires:       %{name} = %{version}-%{release}
%description lang
This subpackage provides with language releated files and locales for gawk.

%prep
%autosetup -n %{name}-%{version} -S git

%build
autoreconf -fv
%configure
%make_build
%make_build -C doc pdf
mkdir -p html/gawk html/gawkinet
makeinfo --html -I doc -o html/gawk     doc/gawk.texi
makeinfo --html -I doc -o html/gawkinet doc/gawkinet.texi

%check
make check

%install
%make_install

rm -f ${RPM_BUILD_ROOT}%{_bindir}/gawk-%{version}*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

ln -sf gawk ${RPM_BUILD_ROOT}%{_bindir}/awk
ln -sf gawk.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/awk.1.gz
ln -sf /usr/share/awk   ${RPM_BUILD_ROOT}%{_datadir}/gawk
ln -sf /usr/libexec/awk ${RPM_BUILD_ROOT}%{_libexecdir}/gawk

install -m 0755 -d ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/gawk/
install -m 0755 -d ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/gawkinet/
install -m 0644 -p html/gawk/*           ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/gawk/
install -m 0644 -p html/gawkinet/*       ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/gawkinet/
install -m 0644 -p doc/gawk.{pdf,ps}     ${RPM_BUILD_ROOT}%{_docdir}/%{name}
install -m 0644 -p doc/gawkinet.{pdf,ps} ${RPM_BUILD_ROOT}%{_docdir}/%{name}

%files
%doc NEWS README POSIX.STD
%license COPYING
%{_bindir}/*awk
%{_libdir}/*awk
%{_datadir}/*awk
%{_libexecdir}/*awk
%{_sysconfdir}/profile.d/gawk.*

%files devel
%{_includedir}/gawkapi.h

%files help
%doc NEWS POSIX.STD README_d/README.multibyte
%doc %{_docdir}/%{name}/gawk.{pdf,ps}
%doc %{_docdir}/%{name}/gawkinet.{pdf,ps}
%doc %{_docdir}/%{name}/html
%{_mandir}/man{1/*,3/*}
%{_infodir}/*awk*.info*

%files lang
%{_datadir}/locale/*

%changelog
* Sun Jan 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0.1-1
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:update to 5.0.1

* Mon Dec 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.2.1-5
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:quality enhancement synchronization github patch

* Thu Aug 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.2.1-4
- Package Init
