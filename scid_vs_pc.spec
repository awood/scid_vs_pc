%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}

Name:           scid_vs_pc
Version:        4.18.1
Release:        1%{?dist}
Summary:        A chess database application
License:        GPLv2+
URL:            http://sourceforge.net/projects/scidvspc
Source0:        https://sourceforge.net/projects/scidvspc/files/source/%{name}-%{version}.tgz
Source1:        %{name}.desktop
Patch0:         %{name}-exec-names.patch
BuildRequires:  tk-devel
BuildRequires:  tcl
BuildRequires:  desktop-file-utils
BuildRequires:  libX11
BuildRequires:  libstdc++-devel
Requires:       tcl
Requires:       tk

%description
Shane's Chess Information Database is a huge chess toolkit with extensive
database, analysis, and chess-playing features.

Scid vs. PC is a usability and bug-fix fork of Scid. It has extensive interface
fixes and improvements and is fully compatible with Scid's .si4 databases.
Its new features include a rewitten Gamelist, a Computer Tournament, and FICS,
Tree, and Book improvements.

%package sounds
Summary:        Sounds for %{name}
License:        GPLv2+
BuildArch:      noarch
Requires:       tcl-snack
Requires:       %{name} = %{version}-%{release}

%description sounds
This package contains sounds for %{name}.

%package books
Summary:        Opening books for %{name}
License:        GPLv2+ and freely redistributable
# books/{Performance.bin,varied.bin} are freely redistributable
# books/{Elo2400.bin,gm2600.bin} are GPL
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description books
This package contains opening books for %{name}.

%prep
%setup -q
%patch0 -p1

for file in engines/toga/readme.txt; do
    mv $file timestamp
    iconv -f ISO-8859-1 -t UTF-8 -o $file timestamp
    touch -r timestamp $file
    rm -f timestamp
done

%build
./configure \
        OPTIMIZE="%{optflags}" \
        BINDIR=%{_bindir} \
        SHAREDIR=%{_datadir}/%{name} \
        TCL_LIBRARY="-ltcl%{tcl_version}" \
        TK_LIBRARY="-ltk%{tcl_version} -ltcl%{tcl_version}"

# BASH_ENV messes with the include path and with GCC 6 (F24+)
# messing with the include path causes stdlib.h to not be
# found.  See https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/37NHYB3UYTO7K53N3H535MUNVCIDGT3O/
make WARNINGS='-w' LDFLAGS='-lX11' BASH_ENV='' CXXFLAGS="${RPM_OPT_FLAGS}"

%install
mkdir -p %{buildroot}/%{_docdir}/%{name}/ezsmtp
mkdir -p %{buildroot}/%{_licensedir}/%{name}/ezsmtp
mv tcl/contrib/ezsmtp/{ChangeLog,ezsmtp.html,koi8-r-body.txt,README.txt,test_examples.txt} %{buildroot}/%{_docdir}/%{name}/ezsmtp
mv tcl/contrib/ezsmtp/license.txt %{buildroot}/%{_licensedir}/%{name}/ezsmtp

make DESTDIR=%{buildroot} install

desktop-file-install \
        --dir %{buildroot}/%{_datadir}/applications \
        %{SOURCE1}

install -m 755 -d %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps/
install -m 644 -p icons/scid.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/

install -m 755 -d %{buildroot}/%{_datadir}/%{name}/sounds/
install -m 644 -p sounds/*.wav %{buildroot}/%{_datadir}/%{name}/sounds/

install -m 755 -d %{buildroot}/%{_datadir}/%{name}/images/
install -m 644 -p images/* %{buildroot}/%{_datadir}/%{name}/images/

install -m 755 -d %{buildroot}/%{_datadir}/%{name}/photos/

install -m 755 -d %{buildroot}/%{_datadir}/%{name}/fonts
install -m 644 -p fonts/*.ttf %{buildroot}/%{_datadir}/%{name}/fonts/

install -m 755 -d %{buildroot}/%{_datadir}/%{name}/bitmaps/
install -m 644 -p bitmaps/*.gif %{buildroot}/%{_datadir}/%{name}/bitmaps/

install -m 755 -d %{buildroot}/%{_datadir}/%{name}/bitmaps2/
install -m 644 -p bitmaps2/*.gif %{buildroot}/%{_datadir}/%{name}/bitmaps2/

mv COPYING %{buildroot}/%{_licensedir}/%{name}
mkdir %{buildroot}/%{_docdir}/%{name}/{toga,phalanx}
mkdir %{buildroot}/%{_licensedir}/%{name}/{toga,phalanx}

mv engines/toga/readme.txt %{buildroot}/%{_docdir}/%{name}/toga
mv engines/toga/copying.txt %{buildroot}/%{_licensedir}/%{name}/toga
mv engines/phalanx/{HISTORY,README} %{buildroot}/%{_docdir}/%{name}/phalanx
mv engines/phalanx/COPYING %{buildroot}/%{_licensedir}/%{name}/phalanx

# Rename various executables to prevent RPM conflicts with original SCID
mv %{buildroot}/%{_bindir}/{sc_eco,%{name}_eco}
mv %{buildroot}/%{_bindir}/{sc_epgn,%{name}_epgn}
mv %{buildroot}/%{_bindir}/{sc_import,%{name}_import}
mv %{buildroot}/%{_bindir}/{sc_remote,%{name}_remote}
mv %{buildroot}/%{_bindir}/{sc_spell,%{name}_spell}

mv %{buildroot}/%{_bindir}/{pgnfix,%{name}_pgnfix}
mv %{buildroot}/%{_bindir}/{scid,%{name}}
mv %{buildroot}/%{_bindir}/{scidpgn,%{name}_pgn}
mv %{buildroot}/%{_bindir}/{spliteco,%{name}_spliteco}
mv %{buildroot}/%{_bindir}/{tkscid,%{name}_tkscid}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%docdir %{_docdir}/%{name}/
%{_docdir}/%{name}/
%{_licensedir}/%{name}/
%{_datadir}/%{name}/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/128x128/apps/*

%files sounds
%{_datadir}/%{name}/sounds/

%files books
%{_datadir}/%{name}/books/*.bin
%doc books/readme.txt

%changelog
* Tue Feb 20 2018 Alex Wood <awood@redhat.com> 4.18.1-1
- Update to latest upstream. 

* Fri Jan 06 2017 Alex Wood <awood@redhat.com> 4.17-1
- Update to new upstream version.

* Mon Apr 25 2016 Alex Wood <awood@redhat.com> 4.16-3
- Apply patch to address crashes with Stockfish. See BZ 1325013.

* Thu Mar 31 2016 Alex Wood <awood@redhat.com> 4.16-2
- Rename files that conflict with files in the original SCID.

* Tue Mar 29 2016 Alex Wood <awood@redhat.com> 4.16-1
- Initial packaging.  Spec file adopted from original SCID spec.
