%define __jar_repack 0
%define _mancenter    mancenter
%define debug_package %{nil}
%define _prefix      /usr/share
%define _conf_dir    %{_sysconfdir}/%{name}
%define _log_dir     %{_var}/log/%{name}
%define _mancenter_data_dir %{_var}/lib/%{_mancenter}
Summary: Hazelcast package.

Name: hazelcast
Version: 3.6.4
Release: 1
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.service
Source2: %{name}.sysconfig
Source3: %{name}.jmxremote.access
Source4: %{name}.jmxremote.password
Source5: %{_mancenter}.service
Source6: %{_mancenter}.sysconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix:   %{_prefix}
URL:      http://www.hazelcast.com/
License:  ASL 2.0
Packager: Alexey Musev <musa@1c.ru>
Provides: hazelcast
BuildRequires: systemd
BuildArch: noarch
%systemd_requires


%package mancenter
Summary: Hazelcast Mancenter package.
Provides: mancenter
BuildRequires: systemd
BuildArch: noarch
%systemd_requires

%description
Hazelcast server.

%description mancenter
Hazelcast Mancenter server.

%prep
%setup -q

%build
rm -f bin/*bat

%install
mkdir -p %{buildroot}%{_prefix}/%{name}
mkdir -p %{buildroot}%{_prefix}/%{name}/libs
mkdir -p %{buildroot}%{_prefix}/%{_mancenter}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_conf_dir}
mkdir -p %{buildroot}%{_mancenter_data_dir}

install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}-%{_mancenter}.service
install -p -D -m 644 bin/*xml %{buildroot}%{_conf_dir}/
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-%{_mancenter}
install -p -D -m 400 %{SOURCE3} %{buildroot}%{_conf_dir}/jmxremote.access
install -p -D -m 400 %{SOURCE4} %{buildroot}%{_conf_dir}/jmxremote.password
install -p -D -m 644 lib/%{name}-all-%{version}.jar %{buildroot}%{_prefix}/%{name}/
install -p -D -m 644 %{_mancenter}/%{_mancenter}-%{version}.war %{buildroot}%{_prefix}/%{_mancenter}/

sed s#FNAME#%{_mancenter}-%{version}.war# -i %{buildroot}%{_unitdir}/%{name}-%{_mancenter}.service
sed s#DATADIR#%{_mancenter_data_dir}# -i %{buildroot}%{_sysconfdir}/sysconfig/%{name}-%{_mancenter}

%clean
rm -rf %{buildroot}

%pre
/usr/bin/getent group hazelcast >/dev/null || /usr/sbin/groupadd -r hazelcast
if ! /usr/bin/getent passwd hazelcast >/dev/null ; then
    /usr/sbin/useradd -r -g hazelcast -M -d %{_prefix}/%{name} -s /sbin/nologin -c "hazelcast user daemon" hazelcast
fi

%pre mancenter
/usr/bin/getent group mancenter >/dev/null || /usr/sbin/groupadd -r mancenter
if ! /usr/bin/getent passwd mancenter >/dev/null ; then
    /usr/sbin/useradd -r -g mancenter -M -d %{_prefix}/%{_mancenter} -s /sbin/nologin -c "mancenter user daemon" mancenter
fi

%post
%systemd_post %{name}.service

%post mancenter
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%preun mancenter
%systemd_preun %{name}.service

%postun
%systemd_postun

%postun mancenter
%systemd_postun

%files
%defattr(-,root,root)
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0750,root,hazelcast) %dir %{_conf_dir}/
%config(noreplace) %attr(0640,root,hazelcast) %{_conf_dir}/*xml
%config(noreplace) %attr(0400,hazelcast,root) %{_conf_dir}/jmxremote.password
%config(noreplace) %attr(0400,hazelcast,root) %{_conf_dir}/jmxremote.access
%{_prefix}/%{name}
%{_prefix}/%{name}/libs

%files mancenter
%defattr(-,root,root)
%{_unitdir}/%{name}-%{_mancenter}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-%{_mancenter}
%{_prefix}/%{_mancenter}
%attr(750,mancenter,mancenter) %{_mancenter_data_dir}
