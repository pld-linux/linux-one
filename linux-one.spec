# NOTE: currently obsolete, One is built from linux-fusion package
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)
#
%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		rel	18.1
%define		pname	linux-one
Summary:	One IPC Linux kernel module
Summary(pl.UTF-8):	Moduł IPC One dla jądra Linuksa
Name:		%{pname}%{_alt_kernel}
Version:	1.6.0
Release:	%{rel}
License:	GPL v2+
Group:		Base/Kernel
# when packaged in DirectFB tarball
#Source0:	http://www.directfb.org/downloads/Core/DirectFB/DirectFB-%{version}.tar.gz
# but currently:
# $ git clone git://git.directfb.org/git/directfb/core/DirectFB.git DirectFB.git
# $ tar cf linux-one.tar -C DirectFB.git/lib/One linux-one
Source0:	%{pname}.tar.xz
# Source0-md5:	d794442fccb99b82c9c3d0b2d5609aaa
Source1:	OneTypes.h
URL:		http://www.directfb.org/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
One IPC Linux kernel module.

Linux One is the new IPC API used by Coma.

%description -l pl.UTF-8
Moduł IPC One dla jądra Linuksa.

Linux One to nowe API IPC wykorzystywane przez Comę.

%package devel
Summary:	Header file for One IPC device
Summary(pl.UTF-8):	Plik nagłówkowy dla urządzenia IPC One
Group:		Development/Libraries
Requires:	linux-libc-headers

%description devel
Header file for One IPC device.

Linux One is the new IPC API used by Coma.

%description devel -l pl.UTF-8
Plik nagłówkowy dla urządzenia IPC One.

Linux One to nowe API IPC wykorzystywane przez Comę.

%package -n kernel%{_alt_kernel}-misc-one
Summary:	One IPC module for Linux kernel
Summary(pl.UTF-8):	Moduł IPC One dla jądra Linuksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Obsoletes:	kernel-one

%description -n kernel%{_alt_kernel}-misc-one
One IPC module for Linux kernel.

Linux One is the new IPC API used by Coma.

%description -n kernel%{_alt_kernel}-misc-one -l pl.UTF-8
Moduł IPC One dla jądra Linuksa.

Linux One to nowe API IPC wykorzystywane przez Comę.

%prep
%setup -q -n %{pname}

sed -i -e 's/^obj-[^ ]*/obj-m/' src/Makefile-2.6
echo "EXTRA_CFLAGS = -I`pwd`/include -I`pwd`/src/single" >> src/Makefile-2.6

cp %{SOURCE1} include

%build
%if %{with kernel}
cd src
ln -sf Makefile-2.6 Makefile
# NOTE: build_kernel_modules (as of rpm macros 1.649) doesn't allow line breaking
%build_kernel_modules -m linux-one ONECORE=single
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_includedir}/linux
install include/linux/one.h $RPM_BUILD_ROOT%{_includedir}/linux
%endif

%if %{with kernel}
cd src
%install_kernel_modules -m linux-one -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-one
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-one
%depmod %{_kernel_ver}

%if %{with userspace}
%files devel
%defattr(644,root,root,755)
%doc README TODO
%{_includedir}/linux/one.h
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-one
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/linux-one.ko*
%endif
