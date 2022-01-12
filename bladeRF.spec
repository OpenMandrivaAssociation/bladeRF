%define bladerf_group bladerf

%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Name:           bladeRF
Version:        2021.10
Release:        1%{?dist}
Summary:        SDR radio receiver
License:        GPL-2.0-only AND AGPL-3.0-or-later
Group:          Productivity/Hamradio/Other
URL:            https://nuand.com/
#Git-Clone:     https://github.com/Nuand/bladeRF.git
Source0:        https://github.com/Nuand/bladeRF/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	ad9361.tar.xz
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  git-core
BuildRequires:  help2man
BuildRequires:  pkgconfig(libedit)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(udev)

# Although the build scripts mangle the version number to be RPM compatible
# for continuous builds (transforming the output of `git describe`), Fedora 32+
# also validates the version inside the pkgconfig file. There's no impetus for this
# with fish.
%define _wrong_version_format_terminate_build 0

%description
The software for bladeRF USB 3.0 Superspeed Software Defined Radio.

%package -n	%{libname}
Summary:        SDR radio receiver library
Group:          System/Libraries

%description -n	%{libname}
Library for bladeRF, an SDR transceiver.

%package doc
Summary:        Documentation for libbladeRF
Group:          Documentation/HTML

%description doc
HTML documentation files for libbladeRF.

%package udev
Summary:        Udev rules for bladeRF
Group:          Hardware/Other

%description udev
Udev rules for bladeRF.

%package -n	%{devname}
Summary:        Development files for libbladeRF
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{EVRD}

%description -n %{devname}
Libraries and header files for developing applications that want to make
use of libbladerf.

%prep
%autosetup
pushd thirdparty/analogdevicesinc/no-OS
tar -xJf %{SOURCE1}
popd

%build
cd host
%cmake \
  -DUDEV_RULES_PATH=%{_udevrulesdir} \
  -DBLADERF_GROUP=%{bladerf_group} \
%if 0%{?use_syslog}
  -DENABLE_LIBBLADERF_SYSLOG=ON \
%endif
  -DBUILD_DOCUMENTATION=ON
%make_build

%install
cd host
%make_install -C build

#move docs
mkdir -p %{buildroot}%{_docdir}

%pre udev
getent group %{bladerf_group} >/dev/null || groupadd -r %{bladerf_group}

%files
%license COPYING
%doc README.md CONTRIBUTORS
%{_bindir}/bladeRF-cli
%{_bindir}/bladeRF-fsk
%{_mandir}/man1/bladeRF-cli.1.*

%files udev
%{_udevrulesdir}/88-nuand-*.rules

%files -n %{libname}
%{_libdir}/libbladeRF.so*

%files doc
%{_docdir}/libbladeRF

%files -n %{devname}
%{_libdir}/libbladeRF.so*
%{_includedir}/bladeRF1.h
%{_includedir}/bladeRF2.h
%{_includedir}/libbladeRF.h
%{_libdir}/pkgconfig/libbladeRF.pc
