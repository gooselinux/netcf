Name:           netcf
Version:        0.1.6
Release:        4%{?dist}%{?extra_release}
Summary:        Cross-platform network configuration library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://fedorahosted.org/netcf/
Source0:        https://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  readline-devel augeas-devel >= 0.5.2
BuildRequires:  libxml2-devel libxslt-devel
BuildRequires:  libnl-devel
Requires:       %{name}-libs = %{version}-%{release}

%description
A library for modifying the network configuration of a system. Network
configurations are expresed in a platform-independent XML format, which
netcf translates into changes to the system's 'native' network
configuration files.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

Patch01: netcf-0.1.6-bond-make-miimon-arpmon-optional.patch
Patch02: netcf-0.1.6-empty-iptables.patch
Patch03: netcf-0.1.6-handle-quoted-entries.patch
Patch04: netcf-0.1.6-install-sysconfig.aug.patch
Patch05: netcf-0.1.6-dont-delete-physical-on-vlan-define.patch

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description    libs
The libraries for %{name}.

%prep
%setup -q

%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/ncftool

%files libs
%defattr(-,root,root,-)
%{_datadir}/netcf
%{_libdir}/*.so.*
%doc AUTHORS COPYING NEWS

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/netcf.pc

%changelog
* Tue Jul 27 2010 Laine Stump <laine@redhat.com> - 0.1.6-4
- install missing sysconfig.aug file
- Resolves: rhbz#613886
- Don't delete the physical interface config when defining a vlan
- Resolves: rhbz#585112

* Mon Jul 19 2010 Laine Stump <laine@redhat.com> - 0.1.6-3
- properly handle quoted entries in sysconfig files
- Resolves: rhbz#613886

* Tue Jun 29 2010 Laine Stump <laine@redhat.com> - 0.1.6-2
- make miimon/arpmon in bond definitions optional
- Resolves: rhbz#585108
- properly deal with initializing a 0 length /etc/sysconfig/iptables file
- Resolves: rhbz#582905

* Thu Apr 22 2010 Laine Stump <laine@redhat.com> - 0.1.6-1
- New version

* Mon Nov 30 2009 David Lutterkort <lutter@redhat.com> - 0.1.5-1
- New version

* Thu Nov  5 2009 David Lutterkort <lutter@redhat.com> - 0.1.4-1
- New version

* Tue Oct 27 2009 David Lutterkort <lutter@redhat.com> - 0.1.3-1
- New version

* Fri Sep 25 2009 David Lutterkort <lutter@redhat.com> - 0.1.2-1
- New Version

* Wed Sep 16 2009 David Lutterkort <lutter@redhat.com> - 0.1.1-1
- Remove patch netcf-0.1.0-fix-initialization-of-libxslt.patch,
  included upstream

* Tue Sep 15 2009 Mark McLoughlin <markmc@redhat.com> - 0.1.0-3
- Fix libvirtd segfault caused by libxslt init issue (#523382)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 David Lutterkort <lutter@redhat.com> - 0.1.0-1
- BR on augeas-0.5.2
- Drop explicit requires for augeas-libs

* Wed Apr 15 2009 David Lutterkort <lutter@redhat.com> - 0.0.2-1
- Updates acording to Fedora review

* Fri Feb 27 2009 David Lutterkort <lutter@redhat.com> - 0.0.1-1
- Initial specfile
