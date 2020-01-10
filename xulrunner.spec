# Use system sqlite?
%define system_sqlite     0

# Use system nss/nspr?
%define system_nss        1

# Enable webm for i686/x86_64 only
%ifarch %{ix86} x86_64
%define enable_webm       1
%else
%define enable_webm       0
%endif

# Build as a debug package?
%define debug_build       0

# Do we build a final version?
%define official_branding 1

# Minimal required versions
%if %{?system_nss}
%define nspr_version 4.9.2
%define nss_version 3.14.0
%endif

%define cairo_version 1.6.0
%define freetype_version 2.1.9
# gecko_dir_ver should be set to the version in our directory names
# alpha_version should be set to the alpha number if using an alpha, 0 otherwise
# beta_version  should be set to the beta number if using a beta, 0 otherwise
# rc_version    should be set to the RC number if using an RC, 0 otherwise
%global gecko_dir_ver %{version}
%global alpha_version 0
%global beta_version  0
%global rc_version    0

%global mozappdir         %{_libdir}/%{name}

%if %{?system_sqlite}
%define sqlite_version 3.6.22
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%global tarballdir  mozilla-esr17
%global ext_version esr

%if %{alpha_version} > 0
%global pre_version a%{alpha_version}
%global pre_name    alpha%{alpha_version}
%global tarballdir  mozilla-aurora
%endif
%if %{beta_version} > 0
%global pre_version b%{beta_version}
%global pre_name    beta%{beta_version}
%global tarballdir  mozilla-beta
%endif
%if %{rc_version} > 0
%global pre_version rc%{rc_version}
%global pre_name    rc%{rc_version}
%global tarballdir  mozilla-release
%global ext_version esr
%endif
%if %{defined pre_version}
%global gecko_verrel %{expand:%%{version}}-%{pre_name}
%global pre_tag .%{pre_version}
%else
%global gecko_verrel %{expand:%%{version}}
%endif

Summary:        XUL Runtime for Gecko Applications
Name:           xulrunner
Version:        17.0.6
Release:        2%{?pre_tag}%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
# You can get sources at ftp://ftp.mozilla.org/pub/firefox/releases/%{version}%{?pre_version}/source
Source0:        firefox-%{version}%{?pre_version}%{?ext_version}.source.tar.bz2
Source10:       %{name}-mozconfig
Source12:       %{name}-redhat-default-prefs.js
Source21:       %{name}.sh.in
Source23:       %{name}.1
Source100:      find-external-requires

# Xulrunner patches
# Build patches
Patch1:         mozilla-build.patch
Patch2:         xulrunner-install-dir.patch
Patch16:        xulrunner-2.0-chromium-types.patch
Patch17:        camelia.patch
Patch18:        xulrunner-nasm-webm.patch
Patch20:        xulrunner-17.0-jemalloc-ppc.patch
Patch24:        mozilla-abort.patch
Patch25:        xulrunner-secarch.patch

# RHEL specific patches
Patch50:        add-gtkmozembed-17.0.patch
Patch51:        mozilla-193-pkgconfig.patch
# Solves runtime crash of yelp:
Patch53:        mozilla-720682-jemalloc-missing.patch
Patch54:        rhbz-872752.patch

# RHEL6 specific patches
Patch100:       mozilla-gcc-4.4.patch

# Upstream patches
Patch401:       mozilla-746112.patch
Patch403:       mozilla-791626.patch

# ---------------------------------------------------

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%if %{?system_nss}
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%endif
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libnotify-devel
BuildRequires:  autoconf213
BuildRequires:  mesa-libGL-devel

Requires:       liberation-fonts-common
Requires:       liberation-sans-fonts

%if %{?system_nss}
Requires:       nspr >= %{nspr_version}
Requires:       nss >= %{nss_version}
%endif

# RHEL6 BuildRequires and Requires
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  hunspell-devel
Requires:       mozilla-filesystem
%if %{?system_sqlite}
BuildRequires:  sqlite-devel >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%if %{?enable_webm}
BuildRequires:  nasm
%endif

Provides:       gecko-libs = %{gecko_verrel}
Provides:       gecko-libs%{?_isa} = %{gecko_verrel}
Conflicts:      firefox < 3.6

%description
XULRunner is a Mozilla runtime package that can be used to bootstrap XUL+XPCOM
applications that are as rich as Firefox and Thunderbird. It provides mechanisms
for installing, upgrading, and uninstalling these applications. XULRunner also
provides libxul, a solution which allows the embedding of Mozilla technologies
in other projects and products.

%package devel
Summary: Development files for Gecko
Group: Development/Libraries
Obsoletes: mozilla-devel < 1.9
Obsoletes: firefox-devel < 2.1
Obsoletes: xulrunner-devel-unstable
Provides: gecko-devel = %{gecko_verrel}
Provides: gecko-devel%{?_isa} = %{gecko_verrel}
Provides: gecko-devel-unstable = %{gecko_verrel}
Provides: gecko-devel-unstable%{?_isa} = %{gecko_verrel}

Requires: xulrunner = %{version}-%{release}
%if %{?system_nss}
Requires: nspr-devel >= %{nspr_version}
Requires: nss-devel >= %{nss_version}
%endif
Requires: libjpeg-devel
Requires: zip
Requires: bzip2-devel
Requires: zlib-devel
Requires: libIDL-devel
Requires: gtk2-devel
Requires: gnome-vfs2-devel
Requires: libgnome-devel
Requires: libgnomeui-devel
Requires: krb5-devel
Requires: pango-devel
Requires: freetype-devel >= %{freetype_version}
Requires: libXt-devel
Requires: libXrender-devel
Requires: startup-notification-devel
Requires: alsa-lib-devel
Requires: libnotify-devel
# RHEL6 specific Requires:
Requires: cairo-devel >= %{cairo_version}
Requires: hunspell-devel
Requires: sqlite-devel

%description devel
This package contains the libraries amd header files that are needed
for writing XUL+XPCOM applications with Mozilla XULRunner and Gecko.

#---------------------------------------------------------------------
# Override internal dependency generator to avoid showing libraries provided by this package
# in dependencies:
AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%prep
%setup -q -c
cd %{tarballdir}

%patch1  -p1 -b .build
%patch2  -p1

%patch16 -p2 -b .chromium-types
%patch17 -p1 -b .camelia
%if %{?enable_webm}
%patch18 -p0 -b .webm
%endif
%patch20 -p2 -b .jemalloc-ppc

%patch24 -p1 -b .abort
%patch25 -p2 -b .secarch

%patch50 -p2 -b .gtkmozembed
%patch51 -p2 -b .pk
%patch53 -p1 -b .jemalloc-missing
%patch54 -p2 -b .embedlink

%patch100 -p1 -b .gcc-4.4
%patch401 -p2 -b .746112
%patch403 -p1 -b .791626

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?enable_webm}
echo "ac_add_options --without-system-libvpx" >> .mozconfig
echo "ac_add_options --enable-webm" >> .mozconfig
echo "ac_add_options --enable-webrtc" >> .mozconfig
echo "ac_add_options --enable-ogg" >> .mozconfig
%else
echo "ac_add_options --without-system-libvpx" >> .mozconfig
echo "ac_add_options --disable-webm" >> .mozconfig
echo "ac_add_options --disable-webrtc" >> .mozconfig
echo "ac_add_options --disable-ogg" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-methodjit" >> .mozconfig
echo "ac_add_options --disable-monoic" >> .mozconfig
echo "ac_add_options --disable-polyic" >> .mozconfig
echo "ac_add_options --disable-tracejit" >> .mozconfig
%endif

# RHEL 6 mozconfig changes:
echo "ac_add_options --enable-system-hunspell" >> .mozconfig
echo "ac_add_options --enable-libnotify" >> .mozconfig
echo "ac_add_options --enable-startup-notification" >> .mozconfig
echo "ac_add_options --enable-jemalloc" >> .mozconfig

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x ppc ppc64
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

# Debug build flags
%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
echo "ac_add_options --disable-debug" >> .mozconfig
echo "ac_add_options --enable-optimize" >> .mozconfig
%endif

#---------------------------------------------------------------------

%build
%if %{?system_sqlite}
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

cd %{tarballdir}

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS -fpermissive" | %{__sed} -e 's/-Wall//')
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
%endif
%ifarch s390 %{arm} ppc
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif

export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
%ifnarch ppc ppc64 s390 s390x
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

#---------------------------------------------------------------------

%install
cd %{tarballdir}
%{__rm} -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT make -C objdir install STAGE_SDK=1

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} -e 's,RPM_VERREL,%{version}-%{release},g' > rh-default-prefs
%{__install} -p -D -m 644 rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/all-redhat.js
%{__rm} rh-default-prefs

# Start script install
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__cat} %{SOURCE21} | %{__sed} -e 's,XULRUNNER_VERSION,%{gecko_dir_ver},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -f $RPM_BUILD_ROOT%{mozappdir}/%{name}-config

# Copy pc files (for compatibility with 1.9.1)
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc

# Fix multilib devel conflicts...
%ifarch x86_64 ia64 s390x ppc64
%define mozbits 64
%else
%define mozbits 32
%endif

function install_file() {
genheader=$*
mv ${genheader}.h ${genheader}%{mozbits}.h
cat > ${genheader}.h << EOF
/* This file exists to fix multilib conflicts */
#if defined(__x86_64__) || defined(__ia64__) || defined(__s390x__) || defined(__powerpc64__)
#include "${genheader}64.h"
#else
#include "${genheader}32.h"
#endif
EOF
}

INTERNAL_APP_NAME=%{name}-%{gecko_dir_ver}

# Install 32 and 64 bit headers separatelly due to multilib conflicts:
pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_NAME}
install_file "mozilla-config"
popd

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_NAME}
install_file "js-config"
popd

# Link libraries in sdk directory instead of copying them:
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{gecko_dir_ver}/sdk/lib
for i in *.so; do
     rm $i
     ln -s %{mozappdir}/$i $i
done
popd

# Library path
LD_SO_CONF_D=%{_sysconfdir}/ld.so.conf.d
LD_CONF_FILE=xulrunner-%{mozbits}.conf

%{__mkdir_p} ${RPM_BUILD_ROOT}${LD_SO_CONF_D}
%{__cat} > ${RPM_BUILD_ROOT}${LD_SO_CONF_D}/${LD_CONF_FILE} << EOF
%{mozappdir}
EOF

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}

# Use the system hunspell dictionaries for RHEL6+
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Remove tmp files
find $RPM_BUILD_ROOT/%{mozappdir} -name '.mkdir.done' -exec rm -rf {} \;

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
fi

%files
%defattr(-,root,root,-)
%{_bindir}/xulrunner
%dir %{mozappdir}
%doc %attr(644, root, root) %{mozappdir}/LICENSE
%doc %attr(644, root, root) %{mozappdir}/README.xulrunner
%{mozappdir}/chrome
%{mozappdir}/chrome.manifest
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.manifest
%{mozappdir}/defaults
%{mozappdir}/omni.ja
%{mozappdir}/plugins
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/run-mozilla.sh
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
%{mozappdir}/dictionaries
%{mozappdir}/plugin-container
%if !%{?system_nss}
%{mozappdir}/*.chk
%endif

%files devel
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}-devel-*
%{_datadir}/idl/%{name}*%{gecko_dir_ver}
%{_includedir}/%{name}*%{gecko_dir_ver}
%{_libdir}/%{name}-devel-*/*
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell

#---------------------------------------------------------------------

%changelog
* Fri May 10 2013 Martin Stransky <stransky@redhat.com> - 17.0.6-2
- Update to 17.0.6 ESR

* Thu Apr 18 2013 Martin Stransky <stransky@redhat.com> - 17.0.5-2
- Updated nss and nspr versions

* Fri Mar 29 2013 Jan Horak <jhorak@redhat.com> - 17.0.5-1
- Update to 17.0.5 ESR

* Tue Mar 12 2013 Martin Stransky <stransky@redhat.com> - 17.0.3-3
- Added fix for rhbz#916180 - Wrong library directory reference 
  in /usr/bin/xulrunner

* Thu Mar 7 2013 Martin Stransky <stransky@redhat.com> - 17.0.3-2
- Added fix for #848644

* Sat Feb 16 2013 Jan Horak <jhorak@redhat.com> - 17.0.3-1
- Update to 17.0.3 ESR

* Tue Jan 15 2013 Martin Stransky <stransky@redhat.com> - 17.0.2-5
- Fixed NetworkManager preferences
- Added fix for NM regression (mozbz#791626)

* Fri Jan 11 2013 Martin Stransky <stransky@redhat.com> - 17.0.2-2
- Added fix for rhbz#816234 - NFS fix

* Thu Jan 10 2013 Jan Horak <jhorak@redhat.com> - 17.0.2-1
- Update to 17.0.2 ESR

* Fri Nov 30 2012 Jan Horak <jhorak@redhat.com> - 17.0.1-3
- Update to 17.0.1 ESR

* Mon Nov 19 2012 Martin Stransky <stransky@redhat.com> 17.0-1
- Update to 17.0 ESR

* Tue Nov 8 2012 Martin Stransky <stransky@redhat.com> 17.0-0.6.b5
- Update to 17 Beta 5
- Updated fix for rhbz#872752 - embeded crash

* Tue Nov 6 2012 Martin Stransky <stransky@redhat.com> 17.0-0.5.b4
- Added fix for rhbz#872752 - embeded crash

* Thu Nov 1 2012 Martin Stransky <stransky@redhat.com> 17.0-0.4.b4
- Update to 17 Beta 4

* Wed Oct 24 2012 Martin Stransky <stransky@redhat.com> 17.0-0.3.b3
- Update to 17 Beta 3
- Updated ppc(64) patch (mozbz#746112)

* Wed Oct 24 2012 Martin Stransky <stransky@redhat.com> 17.0-0.2.b2
- Built with system nspr/nss

* Fri Oct 19 2012 Martin Stransky <stransky@redhat.com> 17.0-0.1.b2
- Update to 17 Beta 2

* Wed Oct 10 2012 Martin Stransky <stransky@redhat.com> 17.0-0.1.b1
- Update to 17 Beta 1

* Sat Aug 25 2012 Jan Horak <jhorak@redhat.com> - 10.0.7-1
- Update to 10.0.7 ESR

* Thu Aug 16 2012 Martin Stransky <stransky@redhat.com> 10.0.6-2
- Added fix for rhbz#770276 - Firefox segfaults, should
  have a font dependency

* Sat Jul 14 2012 Martin Stransky <stransky@redhat.com> 10.0.6-1
- Update to 10.0.6 ESR

* Tue Jun 26 2012 Martin Stransky <stransky@redhat.com> 10.0.5-3
- Added fix for rhbz#808136 (mozbz#762301)

* Tue Jun 12 2012 Martin Stransky <stransky@redhat.com> 10.0.5-2
- Enabled WebM (rhbz#798880)

* Fri Jun 1 2012 Martin Stransky <stransky@redhat.com> 10.0.5-1
- Update to 10.0.5 ESR

* Tue May 29 2012 Martin Stransky <stransky@redhat.com> 10.0.4-2
- Added patch for mozbz#703633

* Sat Apr 21 2012 Martin Stransky <stransky@redhat.com> 10.0.4-1
- Update to 10.0.4 ESR

* Wed Apr 18 2012 Martin Stransky <stransky@redhat.com> 10.0.3-3
- Fixed mozbz#746112 - ppc(64) freeze

* Mon Apr 2 2012 Kai Engert <kaie@redhat.com> 10.0.3-2
- Fixed mozbz#681937

* Mon Mar 5 2012 Martin Stransky <stransky@redhat.com> 10.0.3-1
- Update to 10.0.3 ESR

* Thu Feb 16 2012 Jan Horak <jhorak@redhat.com> - 10.0.1-2
- Fixed mozbz#727401

* Thu Feb  9 2012 Jan Horak <jhorak@redhat.com> - 10.0.1-1
- Update to 10.0.1 ESR

* Tue Feb 7 2012 Martin Stransky <stransky@redhat.com> 10.0-5
- Update to 10.0 ESR

* Sun Jan 29 2012 Martin Stransky <stransky@redhat.com> 10.0-4
- Update to 10.0

* Thu Jan 19 2012 Martin Stransky <stransky@redhat.com> 10.0-0.3.b5
- Update to 10.0 beta 5

* Wed Jan 18 2012 Martin Stransky <stransky@redhat.com> 10.0-0.2.b4
- Update to 10.0 beta 4

* Thu Jan 12 2012 Jan Horak <jhorak@redhat.com> - 10.0-0.1.b3
- Update to 10.0 beta 3

* Tue Jan  3 2012 Jan Horak <jhorak@redhat.com> - 9.0.1-1
- Update to 9.0.1

* Mon Nov 21 2011 Martin Stransky <stransky@redhat.com> 8.0-6
- Updated to 8.0

* Fri Oct 14 2011 Martin Stransky <stransky@redhat.com> 8.0-5
- Updated to 8.0 Beta 3

* Tue Oct 11 2011 Martin Stransky <stransky@redhat.com> 8.0-4
- Added gtkmozembed patch

* Fri Oct 7 2011 Martin Stransky <stransky@redhat.com> 8.0-3
- Updated to 8.0 Beta 2

* Mon Oct 3 2011 Martin Stransky <stransky@redhat.com> 8.0-2
- Updated to 8.0 Beta 1

* Mon Sep 26 2011 Martin Stransky <stransky@redhat.com> 7.0-7
- Updated to 7.0

* Mon Sep 19 2011 Jan Horak <jhorak@redhat.com> - 7.0-6.b6
- Updated to 7.0 Beta 6
- Added fix for mozbz#674522: s390x javascript freeze fix

* Wed Sep 14 2011 Martin Stransky <stransky@redhat.com> 7.0-2.b5
- Updated to 7.0 Beta 5

* Fri Sep 2 2011 Martin Stransky <stransky@redhat.com> 7.0-1.b4
- Updated to 7.0 Beta 4
- Added ability to build with in-tree nss

* Tue Jul 21 2011 Martin Stransky <stransky@redhat.com> 5.0-2
- Disabled jemalloc on s390(x)
- Fixed nss/nspr min versions

* Tue Jun 28 2011 Martin Stransky <stransky@redhat.com> 5.0-1
- Update to 5.0

* Mon Jun 13 2011 Jan Horak <jhorak@redhat.com> - 1.9.2.18-2
- Update to 1.9.2.18

* Thu Apr 21 2011 Jan Horak <jhorak@redhat.com> - 1.9.2.17-4
- Rebuild

* Fri Apr 15 2011 Jan Horak <jhorak@redhat.com> - 1.9.2.17-3
- Update to 1.9.2.17

* Fri Mar 18 2011 Jan Horak <jhorak@redhat.com> - 1.9.2.15-2
- Fixed mozbz#642395

* Tue Mar  8 2011 Jan Horak <jhorak@redhat.com> - 1.9.2.15-1
- Update to 1.9.2.15

* Mon Feb 21 2011 Jan Horak <jhorak@redhat.com> - 1.9.2.14-3
- Update to build3

* Tue Feb  8 2011 Jan Horak <jhorak@redhat.com> - 1.9.2.14-2
- Update to build2

* Tue Jan 25 2011 Jan Horak <jhorak@redhat.com> - 1.9.2.14-1
- Update to 1.9.2.14

* Mon Dec  6 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.13-3
- Update to 1.9.2.13 build3

* Thu Dec  2 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.13-2
- Update to 1.9.2.13 build2

* Wed Nov 24 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.13-1
- Update to 1.9.2.13

* Wed Oct 27 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.12-1
- Update to 1.9.2.12

* Tue Oct  5 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.11-1
- Update to 1.9.2.11

* Wed Aug 25 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.9-1
- Update to 1.9.2.9

* Fri Jul 23 2010 Christopher Aillon <caillon@redhat.com> - 1.9.2.8-1
- Update to 1.9.2.8

* Wed Jul 14 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.7-2
- Update to build 2

* Thu Jul  1 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.7-1
- Update to 1.9.2.7

* Wed Jun 30 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.6-1
- Update to 1.9.2.6

* Thu Jun 24 2010 Christopher Aillon <caillon@redhat.com> - 1.9.2.4-10
- Printing patches from upstream
- Enable startup notication

* Mon Jun 14 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.4-6
- Update to 1.9.2.4 build 7

* Tue Jun 1 2010 Martin Stransky <stransky@redhat.com> 1.9.2.4-5
- Update to 1.9.2.4 build 6

* Tue May 25 2010 Martin Stransky <stransky@redhat.com> 1.9.2.4-4
- Update to 1.9.2.4 build 5

* Mon May 17 2010 Martin Stransky <stransky@redhat.com> 1.9.2.4-3
- Update to 1.9.2.4 build 4
- Fixed mozbz#546270 patch

* Fri May  7 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.4-2
- Update to 1.9.2.4 build 3

* Tue May 4 2010 Martin Stransky <stransky@redhat.com> 1.9.2.4-1
- Update to 1.9.2.4

* Mon Apr 12 2010 Martin Stransky <stransky@redhat.com> 1.9.2.3-2
- Added fix for rhbz#555760 -  Firefox Javascript anomily,
  landscape print orientation reverts to portrait (mozbz#546270)

* Fri Apr 2 2010 Martin Stransky <stransky@redhat.com> - 1.9.2.3-1
- Update to 1.9.2.3

* Wed Mar 17 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.2-1
- Update to 1.9.2.2

* Wed Feb 17 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-2
- Added fix for #564184 - xulrunner-devel multilib conflict

* Fri Jan 22 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-1
- Update to 1.9.2.1

* Wed Jan 18 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.10.rc1
- Update to 1.9.2.1 RC2

* Wed Jan 13 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.9.rc1
- Update to 1.9.2.1 RC1

* Mon Dec 21 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.8.b5
- Update to 1.9.2.1 Beta 5

* Thu Dec 17 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.7.b4
- Added fix for mozbz#543585 - jemalloc alignment assertion 
  and abort on Linux

* Thu Dec 3 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.6.b4
- Added fix for #543585 - mozilla-plugin.pc contains incorrect CFLAGS

* Fri Nov 27 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.5.b4
- Update to 1.9.2.1 Beta 4

* Mon Nov 23 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.4.b3
- added -unstable.pc files for compatibility with 1.9.1

* Fri Nov 20 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.3.b3
- Necko wifi monitor disabled
- fixed a dependency (#539261)
- added source URL (#521704)

* Wed Nov 18 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.2.b3
- Rebase to 1.9.2.1 Beta 3

* Fri Nov 13 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.1.beta2
- Rebase to 1.9.2.1 Beta 2
- fix the sqlite runtime requires again (#480989), add a check 
  that the sqlite requires is sane (by Stepan Kasal)

* Thu Nov  5 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.5-1
- Update to 1.9.1.5

* Mon Oct 26 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.4-1
- Update to 1.9.1.4

* Mon Sep  7 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.3-1
- Update to 1.9.1.3

* Fri Aug 21 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.2-4
- Added libnotify support

* Wed Aug 12 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-3
- Added fix from #516118 - Headers not C89

* Mon Aug 6 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-2
- Rebuilt

* Mon Aug 3 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-1
- Update to 1.9.1.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Christopher Aillon <caillon@redhat.com> - 1.9.1.1-1
- Update to 1.9.1.1

* Mon Jul 13 2009 Jan Horak <jhorak@redhat.com> - 1.9.1-3
- Fixed wrong version of Firefox when loading 'about:' as location
- Added patch to compile against latest GTK

* Tue Jun 30 2009 Yanko Kaneti <yaneti@declera.com> - 1.9.1-2
- Build using system hunspell

* Tue Jun 30 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-1
- Update to 1.9.1 final release

* Wed Jun 24 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.23
- Rebuilt because of gcc update (#506952)

* Thu Jun 18 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.22
- Backed out last change, it does not work inside mock (koji)

* Tue Jun 16 2009 Stepan Kasal <skasal@redhat.com> 1.9.1-0.21
- require sqlite of version >= what was used at buildtime (#480989)
- in devel subpackage, drop version from sqlite-devel require; that's
  handled indirectly through the versioned require in main package

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.20
- 1.9.1 beta 4

* Fri Mar 27 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.11
- Add patches for MFSA-2009-12, MFSA-2009-13

* Fri Mar 13 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.10
- 1.9.1 beta 3

* Fri Feb 27 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.9
- Build fix for pango 1.23
- Misc. build fixes

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-0.8.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.7
- Re-enable NM by default

* Wed Jan  7 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.6
- Copied mozilla-config.h to stable include dir (#478445)

* Mon Dec 22 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.5
- Typo fix

* Sat Dec 20 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.4
- 1.9.1 beta 2

* Tue Dec  9 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.3
- Mark this as a pre-release

* Tue Dec  9 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.2
- Add needed -devel requires to the -devel package

* Thu Dec  4 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.1
- 1.9.1 beta 1

* Wed Nov 12 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.4-1
- Update to 1.9.0.4

* Mon Oct 27 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-5
- Password manager fixes from upstream

* Tue Oct  7 2008 Marco Pesenti Gritti <mpg@redhat.com> 1.9.0.2-4
- Add missing dependency on python-devel

* Sun Oct  5 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-3
- Enable PyXPCOM

* Thu Sep 25 2008 Martin Stransky <stransky@redhat.com> 1.9.0.2-2 
- Build with system cairo (#463341)

* Tue Sep 23 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-1
- Update to 1.9.0.2

* Wed Jul 23 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.1-2
- Disable system hunspell for now as it's causing some crashes (447444)

* Wed Jul 16 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.1-1
- Update to 1.9.0.1

* Tue Jun 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-1
- Update to 1.9 final

* Thu May 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.63
- Simplify PS/PDF operators

* Thu May 22 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.62
- Upstream patch to fsync() less

* Thu May 08 2008 Colin Walters <walters@redhat.com> 1.9-0.61
- Ensure we enable startup notification; add BR and modify config
  (bug #445543)

* Wed Apr 30 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.60
- Some files moved to mozilla-filesystem; kill them and add the Req

* Mon Apr 28 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.59
- Clean up the %%files list and get rid of the executable bit on some files

* Sat Apr 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.58
- Fix font scaling

* Fri Apr 25 2008 Martin Stransky <stransky@redhat.com> 1.9-0.57
- Enabled phishing protection (#443403)

* Wed Apr 23 2008 Martin Stransky <stransky@redhat.com> 1.9-0.56
- Changed "__ppc64__" to "__powerpc64__", 
  "__ppc64__" doesn't work anymore
- Added fix for #443725 - Critical hanging bug with fix 
  available upstream (mozbz#429903)

* Fri Apr 18 2008 Martin Stransky <stransky@redhat.com> 1.9-0.55
- Fixed multilib issues, added starting script instead of a symlink
  to binary (#436393)

* Sat Apr 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.54
- Add upstream patches for dpi, toolbar buttons, and invalid keys
- Re-enable system cairo

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.53
- Spec cleanups

* Wed Apr  2 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.52
- Beta 5

* Mon Mar 31 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.51
- Beta 5 RC2

* Thu Mar 27 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.50
- Update to latest trunk (2008-03-27)

* Wed Mar 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.49
- Update to latest trunk (2008-03-26)

* Tue Mar 25 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.48
- Update to latest trunk (2008-03-25)

* Mon Mar 24 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.47
- Update to latest trunk (2008-03-24)

* Thu Mar 20 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.46
- Update to latest trunk (2008-03-20)

* Mon Mar 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.45
- Update to latest trunk (2008-03-17)

* Mon Mar 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.44
- Revert to trunk from the 15th to fix crashes on HTTPS sites

* Sun Mar 16 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.43
- Update to latest trunk (2008-03-16)
- Add patch to negate a11y slowdown on some pages (#431162)

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.42
- Update to latest trunk (2008-03-15)

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.41
- Avoid conflicts between gecko debuginfo packages

* Wed Mar 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.40
- Update to latest trunk (2008-03-12)

* Tue Mar 11 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.39
- Update to latest trunk (2008-03-11)

* Mon Mar 10 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.38
- Update to latest trunk (2008-03-10)

* Sun Mar  9 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.37
- Update to latest trunk (2008-03-09)

* Fri Mar  7 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.36
- Update to latest trunk (2008-03-07)

* Thu Mar  6 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.35
- Update to latest trunk (2008-03-06)

* Tue Mar  4 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.34
- Update to latest trunk (2008-03-04)

* Sun Mar  2 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.33
- Update to latest trunk (2008-03-02)

* Sat Mar  1 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.32
- Update to latest trunk (2008-03-01)

* Fri Feb 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.31
- Update to latest trunk (2008-02-29)

* Thu Feb 28 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.30
- Update to latest trunk (2008-02-28)

* Wed Feb 27 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.29
- Update to latest trunk (2008-02-27)

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.28
- Update to latest trunk (2008-02-26)

* Sat Feb 23 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.27
- Update to latest trunk (2008-02-23)

* Fri Feb 22 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.26
- Update to latest trunk (2008-02-22)

* Thu Feb 21 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.25
- Update to latest trunk (2008-02-21)

* Wed Feb 20 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.24
- Update to latest trunk (2008-02-20)

* Sun Feb 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.23
- Update to latest trunk (2008-02-17)

* Fri Feb 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.22
- Update to latest trunk (2008-02-15)

* Thu Feb 14 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.21
- Update to latest trunk (2008-02-14)
- Use system hunspell

* Mon Feb 11 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.19
- Update to latest trunk (2008-02-11)

* Mon Feb 11 2008 Adam Jackson <ajax@redhat.com> 1.9-0.beta2.19
- STRIP="/bin/true" on the %%make line so xulrunner-debuginfo contains,
  you know, debuginfo.

* Sun Feb 10 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.18
- Update to latest trunk (2008-02-10)

* Sat Feb  9 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.17
- Update to latest trunk (2008-02-09)

* Wed Feb  6 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.16
- Update to latest trunk (2008-02-06)

* Tue Jan 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.15
- Update to latest trunk (2008-01-30)

* Wed Jan 25 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.14
- rebuild agains new nss
- enabled gnome vfs

* Wed Jan 23 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.13
- fixed stable pkg-config files (#429654)
- removed sqlite patch

* Mon Jan 21 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.12
- Update to latest trunk (2008-01-21)

* Tue Jan 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.11
- Update to latest trunk (2008-01-15)
- Now with system extensions directory support

* Sat Jan 13 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.10
- Update to latest trunk (2008-01-13)
- Use CFLAGS instead of configure arguments
- Random cleanups: BuildRequires, scriptlets, prefs, etc.

* Sat Jan 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.9
- Provide gecko-devel-unstable as well

* Wed Jan 9 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.8
- divided devel package to devel and devel-unstable

* Mon Jan 7 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.7
- removed fedora specific pkg-config files
- updated to the latest trunk (2008-01-07)
- removed unnecessary patches
- fixed idl dir (#427965)

* Thu Jan 3 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.6
- Re-enable camellia256 support now that NSS supports it

* Thu Jan 3 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.5
- updated to the latest trunk (2008-01-03)

* Mon Dec 24 2007 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.4
- Don't Provide webclient (xulrunner is not itself a webclient)
- Don't Obsolete old firefox, only firefox-devel
- Kill legacy obsoletes (phoenix, etc) that were never in rawhide

* Thu Dec 21 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.3
- added java and plugin subdirs to plugin includes

* Thu Dec 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.2
- dependency fixes, obsoletes firefox < 3 and firefox-devel now

* Wed Dec 12 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.1
- updated to Beta 2.
- moved SDK to xulrunner-sdk

* Thu Dec 06 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.4
- fixed mozilla-plugin.pc (#412971)

* Tue Nov 27 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.3
- export /etc/gre.d/gre.conf (it's used by python gecko applications)

* Mon Nov 26 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.2
- added xulrunner/js include dir to xulrunner-js

* Tue Nov 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.1
- update to beta 1

* Mon Nov 19 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.6
- packed all gecko libraries (#389391)

* Thu Nov 15 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.5
- registered xulrunner libs system-wide
- added xulrunner-gtkmozembed.pc

* Wed Nov 14 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.4
- added proper nss/nspr dependencies

* Wed Nov 14 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.3
- more build fixes, use system nss libraries

* Tue Nov 6 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.2
- build fixes

* Tue Oct 30 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.1
- updated to the latest trunk

* Thu Sep 20 2007 David Woodhouse <dwmw2@infradead.org> 1.9-0.alpha7.4
- build fixes for ppc/ppc64

* Tue Sep 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha7.3
- removed conflicts with the current gecko-based apps
- added updated ppc64 patch

* Tue Sep 18 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha7.2
- build fixes

* Wed Sep  5 2007 Christopher Aillon <caillon@redhat.com> 1.9-0.alpha7.1
- Initial cut at XULRunner 1.9 Alpha 7
- Temporarily revert camellia 256 support since our nss doesn't support it yet
