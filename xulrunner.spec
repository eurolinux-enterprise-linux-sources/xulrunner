# Use system sqlite?
%define system_sqlite     0
%define system_ffi        1

# Use system nss/nspr?
%define system_nss        1

%define enable_webm       1

# Build as a debug package?
%define debug_build       0

# Do we build a final version?
%define official_branding 1

# Minimal required versions
%if %{?system_nss}
%global nspr_version 4.10.6
%global nss_version 3.16.2.3
%endif

%define cairo_version 1.6.0
%define freetype_version 2.1.9
%define ffi_version 3.0.9
%define libvpx_version 1.3.0

# gecko_dir_ver should be set to the version in our directory names
%global gecko_dir_ver %{version}

%global mozappdir         %{_libdir}/%{name}

%if %{?system_sqlite}
%define sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%global tarballdir  mozilla-esr31
%global ext_version esr
%global gecko_verrel %{expand:%%{version}}

Summary:        XUL Runtime for Gecko Applications
Name:           xulrunner
Version:        31.4.0
Release:        1%{?pre_tag}%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        ftp://ftp.mozilla.org/pub/firefox/releases/%{version}%{?pre_version}/source/firefox-%{version}%{ext_version}%{?pre_version}.source.tar.bz2
Source10:       %{name}-mozconfig
Source12:       %{name}-redhat-default-prefs.js
Source21:       %{name}.sh.in
Source23:       %{name}.1
Source100:      find-external-requires

# Xulrunner patches
# Build patches
Patch0:         xulrunner-nspr-version.patch
Patch2:         firefox-install-dir.patch
Patch6:         webrtc-arch-cpu.patch
Patch20:        xulrunner-24.0-jemalloc-ppc.patch
Patch21:        disable-webm.patch
Patch22:        remove-ogg.patch

# RHEL specific patches
Patch51:        mozilla-193-pkgconfig.patch
# Solves runtime crash of yelp:
Patch54:        rhbz-872752.patch
Patch55:        rhbz-966424.patch

# RHEL specific patches

# Upstream patches

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
BuildRequires:  pulseaudio-libs-devel

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
%if %{?system_ffi}
BuildRequires:  libffi-devel >= %{ffi_version}
Requires:       libffi >= %{ffi_version}
%endif
%if %{?enable_webm}
BuildRequires:  libvpx-devel >= %{libvpx_version}
Requires:       libvpx >= %{libvpx_version}
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

sed -e 's/__RH_NSPR_VERSION__/%{nspr_version}/' %{P:%%PATCH0} > version.patch
%{__patch} -p2 -b --suffix .nspr --fuzz=0 < version.patch

%patch2  -p1
%patch6  -p1 -b .webrtc-arch-cpu
%patch20 -p2 -b .jemalloc-ppc
%if !%{?enable_webm}
%patch21 -p1 -b .disable-webm
%endif
%patch22 -p1 -b .ogg
%patch51 -p2 -b .pk
%patch54 -p2 -b .embedlink
%patch55 -p1 -b .973720

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
echo "ac_add_options --with-system-libvpx" >> .mozconfig
echo "ac_add_options --enable-webm" >> .mozconfig
echo "ac_add_options --enable-webrtc" >> .mozconfig
echo "ac_add_options --enable-ogg" >> .mozconfig
%else
echo "ac_add_options --without-system-libvpx" >> .mozconfig
echo "ac_add_options --disable-webm" >> .mozconfig
echo "ac_add_options --disable-webrtc" >> .mozconfig
echo "ac_add_options --disable-ogg" >> .mozconfig
echo "ac_add_options --disable-opus" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-methodjit" >> .mozconfig
echo "ac_add_options --disable-monoic" >> .mozconfig
echo "ac_add_options --disable-polyic" >> .mozconfig
echo "ac_add_options --disable-tracejit" >> .mozconfig
%endif

echo "ac_add_options --enable-system-hunspell" >> .mozconfig
echo "ac_add_options --enable-libnotify" >> .mozconfig
echo "ac_add_options --enable-startup-notification" >> .mozconfig
echo "ac_add_options --enable-jemalloc" >> .mozconfig

# Debug build flags
%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
echo "ac_add_options --disable-debug" >> .mozconfig
echo "ac_add_options --enable-optimize" >> .mozconfig
%endif

%if %{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
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
function install_file() {
genheader=$*
mv ${genheader}.h ${genheader}%{__isa_bits}.h
cat > ${genheader}.h << EOF
/* This file exists to fix multilib conflicts */
#if defined(__x86_64__) || defined(__ia64__) || defined(__s390x__) || defined(__powerpc64__) || defined(__aarch64__)
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

# Move sdk/bin to xulrunner libdir
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{gecko_dir_ver}/sdk/bin
mv ply *.py $RPM_BUILD_ROOT%{mozappdir}
popd
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{gecko_dir_ver}/sdk/bin
ln -s %{mozappdir} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{gecko_dir_ver}/sdk/bin

# Library path
LD_SO_CONF_D=%{_sysconfdir}/ld.so.conf.d
LD_CONF_FILE=xulrunner-%{__isa_bits}.conf

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
%{mozappdir}/install_app.py
%ghost %{mozappdir}/install_app.pyc
%ghost %{mozappdir}/install_app.pyo

%files devel
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}-devel-*
%{_datadir}/idl/%{name}*%{gecko_dir_ver}
%{_includedir}/%{name}*%{gecko_dir_ver}
%{_libdir}/%{name}-devel-*/*
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell
%{mozappdir}/*.py
%ghost %{mozappdir}/*.pyc
%ghost %{mozappdir}/*.pyo
%dir %{mozappdir}/ply
%{mozappdir}/ply/*.py
%ghost %{mozappdir}/ply/*.pyc
%ghost %{mozappdir}/ply/*.pyo

#---------------------------------------------------------------------

%changelog
* Tue Jan  6 2015 Jan Horak <jhorak@redhat.com> - 31.4.0-1
- Update to 31.4.0 ESR

* Fri Dec 5 2014 Martin Stransky <stransky@redhat.com> - 31.3.0-1
- Update to 31.3.0 ESR Build 2

* Mon Nov 10 2014 Martin Stransky <stransky@redhat.com> - 31.2.0-3
- Ship sdk/bin as a symlink for compability (rhbz#1162187)

* Mon Oct 27 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 31.2.0-2
- Fix webRTC for aarch64, ppc64le (rhbz#1148622)

* Tue Oct  7 2014 Jan Horak <jhorak@redhat.com> - 31.2.0-1
- Update to 31.2.0

* Tue Sep 9 2014 Martin Stransky <stransky@redhat.com> - 31.1.0-3
- move /sdk/bin to xulrunner libdir

* Mon Sep 8 2014 Martin Stransky <stransky@redhat.com> - 31.1.0-2
- Sync preferences with Firefox package

* Mon Sep 8 2014 Martin Stransky <stransky@redhat.com> - 31.1.0-1
- Update to 31.1.0 ESR

* Thu Aug 14 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 31.0-2
- Fix header wrapper for aarch64

* Tue Aug 5 2014 Martin Stransky <stransky@redhat.com> - 31.0-1
- Update to 31.0 ESR

* Wed Jun  4 2014 Jan Horak <jhorak@redhat.com> - 24.6.0-1
- Update to 24.6.0 ESR

* Wed Apr 23 2014 Martin Stransky <stransky@redhat.com> - 24.5.0-1
- Update to 24.5.0 ESR

* Thu Mar 27 2014 Martin Stransky <stransky@redhat.com> - 24.4.0-1
- Update to 24.4.0 ESR

* Wed Feb  5 2014 Jan Horak <jhorak@redhat.com> - 24.3.0-1
- Update to 24.3.0 ESR

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 24.2.0-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 24.2.0-2
- Mass rebuild 2013-12-27

* Mon Dec 9 2013 Martin Stransky <stransky@redhat.com> - 24.2.0-1
- Update to 24.2.0 ESR

* Fri Nov 22 2013 Martin Stransky <stransky@redhat.com> - 24.1.0-2
- Relaxed the nspr dependency

* Wed Nov 6 2013 Martin Stransky <stransky@redhat.com> - 24.1.0-1
- Update to 24.1.0 ESR

* Wed Oct 23 2013 Martin Stransky <stransky@redhat.com> - 24.0-1
- Update to 24.0 ESR

* Thu Sep 12 2013 Jan Horak <jhorak@redhat.com> - 17.0.9-1
- Update to 17.0.9 ESR

* Wed Sep  4 2013 Jan Horak <jhorak@redhat.com> - 17.0.8-5
- Fixed mozbz#633001 - Cannot open ipv6 address with self-signed certificate

* Tue Sep 3 2013 Martin Stransky <stransky@redhat.com> - 17.0.8-4
- Fixed rhbz#818636 - Firefox allows install of addons,
  disregarding xpinstall.enabled flag set as false.

* Tue Aug 6 2013 Martin Stransky <stransky@redhat.com> - 17.0.8-3
- Update to 17.0.8 ESR Build 2

* Thu Aug 1 2013 Martin Stransky <stransky@redhat.com> - 17.0.8-2
- Added fix for rhbz#990921 - firefox does not build with 
  required nss/nspr

* Wed Jul 31 2013 Martin Stransky <stransky@redhat.com> - 17.0.8-1
- Update to 17.0.8 ESR

* Thu Jun 20 2013 Jan Horak <jhorak@redhat.com> - 17.0.7-1
- Update to 17.0.7 ESR

* Tue Jun 18 2013 Jan Horak <jhorak@redhat.com> - 17.0.6-2
- Fixed launch script, rhbz#974006
- Fixed problems with addon installation, rhbz#973720

* Fri May 17 2013 Jan Horak <jhorak@redhat.com> - 17.0.6-1
- Update to 17.0.6 ESR

* Tue Apr  2 2013 Jan Horak <jhorak@redhat.com> - 17.0.5-1
- Update to 17.0.5 ESR

* Wed Mar 13 2013 Martin Stransky <stransky@redhat.com> - 17.0.4-1
- Update to 17.0.4 ESR
- Added fix for mozbz#239254 - [Linux] Support disk cache on a local path
- Use an official firefox tarball

* Tue Jan 15 2013 Martin Stransky <stransky@redhat.com> - 17.0.2-3
- Added fix for NM regression (mozbz#791626)

* Fri Jan 11 2013 Martin Stransky <stransky@redhat.com> - 17.0.2-2
- Added fix for rhbz#816234 - NFS fix

* Thu Jan 10 2013 Jan Horak <jhorak@redhat.com> - 17.0.2-1
- Update to 17.0.2 ESR

* Thu Dec 20 2012 Jan Horak <jhorak@redhat.com> - 17.0.1-1
- Update to 17.0.1 ESR

* Mon Nov 19 2012 Martin Stransky <stransky@redhat.com> 17.0-1
- Update to 17.0 ESR

* Thu Nov 8 2012 Martin Stransky <stransky@redhat.com> 17.0-0.6.b5
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
