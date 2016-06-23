%global         debug_package %{nil}
%global         __strip /bin/true

Name:           nvidia-driver-NVML-devel
Version:        340.29
Release:        1%{?dist}
Summary:        NVIDIA Management Library (NVML) development files
Epoch:          1
License:        NVIDIA License
URL:            https://developer.nvidia.com/nvidia-management-library-nvml
Source0:        http://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_340_29_gdk_linux_32.run
Source1:        http://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_340_29_gdk_linux_64.run

Requires:       nvidia-driver-NVML%{_isa}
Obsoletes:      gpu-deployment-kit%{_isa} < %{?epoch}:%{version}-%{release}
Provides:       gpu-deployment-kit%{_isa} = %{?epoch}:%{version}-%{release}

%description
A C-based API for monitoring and managing various states of the NVIDIA GPU
devices. It provides a direct access to the queries and commands exposed via
nvidia-smi. The run-time version of NVML ships with the NVIDIA display driver,
and the SDK provides the appropriate header, stub libraries and sample
applications. Each new version of NVML is backwards compatible and is intended
to be a platform for building 3rd party applications.

%package -n nvidia-healthmon
Summary:        NVIDIA Tesla Health Monitor

%description -n nvidia-healthmon
System administrator's and cluster manager's tool for detecting and
troubleshooting common problems affecting NVIDIA Tesla GPUs in a high
performance computing environment. It contains limited hardware diagnostic
capabilities, and focuses on software and system configuration issues.

%prep
%setup -c -T -n %{name}-%{version}
%ifarch %{ix86}
sh %{SOURCE0} --installdir=`pwd` --silent 
%endif

%ifarch x86_64
sh %{SOURCE1} --installdir=`pwd` --silent
%endif

rm -fr .%{_bindir}/{.uninstall_manifest_do_not_delete.txt,uninstall_gdk.pl}
mv .%{_prefix}/src/gdk/nvml/examples .
rm -fr .%{_prefix}/src/

%build
# Nothing to build

%install
cp -fr usr etc %{buildroot}

# Compress man pages
for man in %{buildroot}%{_mandir}/man3/* %{buildroot}%{_mandir}/man8/*; do gzip -9 $man; done

%files
%doc examples
%{_includedir}/nvidia/gdk
%{_mandir}/man3/*.3.*

%files -n nvidia-healthmon
%dir %{_sysconfdir}/nvidia-healthmon/
%config(noreplace) %{_sysconfdir}/nvidia-healthmon/nvidia-healthmon.conf
%{_bindir}/nvidia-healthmon
%{_bindir}/nvidia-healthmon-tests
%{_mandir}/man8/nvidia-healthmon.*

%changelog
* Thu Jun 23 2016 Simone Caronni <negativo17@gmail.com> - 1:340.29-1
- Update to 340.29.

* Wed Sep 24 2014 Simone Caronni <negativo17@gmail.com> - 1:340.29-1
- Update to 340.29.

* Wed Aug 20 2014 Simone Caronni <negativo17@gmail.com> - 1:340.21-1
- Update to 340.21.
- Package nvidia-healthmon is now available also on 32 bit.

* Mon Jul 14 2014 Simone Caronni <negativo17@gmail.com> - 1:331.62-1
- First build.
- Create nvidia-healthmon subpackage (x86_64 only).
