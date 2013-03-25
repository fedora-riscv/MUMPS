Name: MUMPS
Version: 4.10.0
Release: 9%{?dist}
Summary: A MUltifrontal Massively Parallel sparse direct Solver
License: Public Domain
Group: Development/Libraries
URL: http://mumps.enseeiht.fr/
Source0: http://mumps.enseeiht.fr/%{name}_%{version}.tar.gz

# Custom Makefile changed for Fedora and built from Make.inc/Makefile.gfortran.PAR in the source.
Source1: %{name}-Makefile.par.inc

# These patches create static and shared versions of pord, sequential and mumps libraries
# They are changed for Fedora and  derive from patches for Debian on 
# http://bazaar.launchpad.net/~ubuntu-branches/ubuntu/raring/mumps/raring/files/head:/debian/patches/
Patch0: %{name}-examples-mpilibs.patch
Patch1: %{name}-shared-pord.patch
Patch2: %{name}-shared.patch

BuildRequires: gcc-gfortran, blas-devel, lapack-devel
BuildRequires: openmpi-devel, scalapack-openmpi-devel, blacs-openmpi-devel
BuildRequires: openssh-clients

%description
MUMPS implements a direct solver for large sparse linear systems, with a
particular focus on symmetric positive definite matrices.  It can
operate on distributed matrices e.g. over a cluster.  It has Fortran and
C interfaces, and can interface with ordering tools such as Scotch.

%package devel
Summary: The MUMPS headers and development-related files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Shared links, header files for MUMPS.

%package doc
Summary: The MUMPS documentation files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description doc
This document describes the Fortran 90 and C user interfaces to 
MUMPS 4.10.0 . It describes in detail the data structures, parameters, 
calling sequences, and error diagnostics. Basic example programs
using MUMPS are also provided.

%package examples
Summary: MUMPS illustrative test programs
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
Illustrative test programs about how MUMPS can be used
See README file

%prep
%setup -q -n %{name}_%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

# Build parallel version.
rm -f Makefile.inc
cp -f %{SOURCE1} Makefile.inc

# Set build flags macro
sed -e 's|@@CFLAGS@@|%{optflags}|g' -i Makefile.inc
sed -e 's|@@-O@@|-Wl,--as-needed|g' -i Makefile.inc

MUMPS_MPI=openmpi
MUMPS_INCDIR=-I/usr/include/openmpi-%{_arch}

MUMPS_LIBF77="\
-L%{_libdir}/openmpi -L%{_libdir}/openmpi/lib \
-lmpi_f77 -lmpi -lscalapack -lmpiblacs \
-lmpiblacsF77init -lmpiblacsCinit -llapack"

make MUMPS_MPI="$MUMPS_MPI" \
     MUMPS_INCDIR="$MUMPS_INCDIR" \
     MUMPS_LIBF77="$MUMPS_LIBF77" \
     all

# Make sure documentation is using Unicode.
iconv -f iso8859-1 -t utf-8 README > README-t && mv README-t README

%check
# Running test programs showing how MUMPS can be used
cd examples

%if 0%{?rhel}
module load %{_sysconfdir}/modulefiles/openmpi-%{_arch}
%else
module load mpi
%endif

LD_LIBRARY_PATH=$PWD:../lib:$LD_LIBRARY_PATH ./ssimpletest < input_simpletest_real
LD_LIBRARY_PATH=$PWD:../lib:$LD_LIBRARY_PATH ./csimpletest < input_simpletest_cmplx
cd ../

%install

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}-examples
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}

# Install documentation
install -cpm 644 README $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

# Install libraries.
install -cpm 755 lib/lib*-*.so $RPM_BUILD_ROOT%{_libdir}

# Install development files.
install -cpm 755 lib/libmumps_common.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 lib/lib*mumps.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 lib/lib*mumps-%{version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 lib/libpord-%{version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 lib/libpord.so $RPM_BUILD_ROOT%{_libdir}

# Make symbolic links instead hard-link 
ln -sf %{_libdir}/libsmumps-%{version}.so $RPM_BUILD_ROOT%{_libdir}/libsmumps.so
ln -sf %{_libdir}/libcmumps-%{version}.so $RPM_BUILD_ROOT%{_libdir}/libcmumps.so
ln -sf %{_libdir}/libzmumps-%{version}.so $RPM_BUILD_ROOT%{_libdir}/libzmumps.so
ln -sf %{_libdir}/libdmumps-%{version}.so $RPM_BUILD_ROOT%{_libdir}/libdmumps.so
ln -sf %{_libdir}/libmumps_common-%{version}.so $RPM_BUILD_ROOT%{_libdir}/libmumps_common.so
ln -sf %{_libdir}/libpord-%{version}.so $RPM_BUILD_ROOT%{_libdir}/libpord.so

install -cpm 644 include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -cpm 755 examples/?simpletest $RPM_BUILD_ROOT%{_libdir}/%{name}-examples
install -cpm 755 examples/input_* $RPM_BUILD_ROOT%{_libdir}/%{name}-examples


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README LICENSE ChangeLog
%{_libdir}/libpord-%{version}.so
%{_libdir}/lib?mumps-%{version}.so
%{_libdir}/libmumps_common-%{version}.so

%files devel
%doc ChangeLog
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/lib?mumps.so
%{_libdir}/libmumps_common.so
%{_libdir}/libpord.so

%files doc
%doc doc/*.pdf

%files examples
%doc examples/README
%dir %{_libdir}/%{name}-examples
%{_libdir}/%{name}-examples/*simpletest
%{_libdir}/%{name}-examples/*_simpletest_*


%changelog
* Sat Mar 23 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-9
- Removed '-Wuninitialized -Wno-maybe-uninitialized' flags because unrecognized
  in EPEL6
- Added condition to load MPI module properly

* Sat Mar 02 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-8
- Removed %%post/%%postun commands for devel sub-package

* Thu Feb 28 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-7
- Exchanged versioned/unversioned libs between main and devel packages
- Set up a doc subpackage that cointains PDF documentation
- Erased .ps documentation
- ChangeLog even in devel package
- SourceX/PatchY prefixed with %%{name}
- Added 'openssh-clients' to BuildRequires

* Wed Feb 27 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-6
- Removed 'libopen-pal.so.4' and 'libopen-rte.so.4' private libraries exclusion
- Imposed '-Wl,--as-needed' flags to the libopen-pal/-rte libs in shared-mumps.patch
- Added '-Wuninitialized -Wno-maybe-uninitialized' in shared-mumps.patch 
  to silence '-Wmaybe-uninizialized' warnings 

* Tue Feb 26 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-5
- Removed sequential version building
- Removed Make.seq.inc file from sources
- Set up of OPT* entries in the Make.par.inc file

* Mon Feb 25 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-4
- Added %%check section

* Mon Feb 25 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-3
- Sequential version's Make command  pointed to openmpi header/lib files
- Set optflags macros

* Fri Feb 22 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-2
- Add '_includedir/MUMPS' directory, header files moved into
- 'Buildroot:' line removed
- Manuals pdf/ps included as %%doc files
- Add a new sub-package 'examples', it contains test files and relative README
- LICENSE and README files in %%doc
- '%%clean section' removed
- 'rm -rf %%{buildroot}' and '%%defattr' lines removed
- Compiler flags included in custom Makefile.par.inc/Makefile.seq.inc files

* Wed Feb 20 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-1
- 'libopen-pal.so.4' and 'libopen-rte.so.4' private libraries exclusion

* Wed Feb 20 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-0
- Remove exec permissions to remove 'script-without-shebang' errors
- Make symbolic links instead hard-link 
- Make sure documentation is using Unicode.
- Add Package patches and custom Makefiles changed for Fedora.
- Initial package.
