%if 0%{?fedora} <= 22
%global _hardened_build 1
%endif

%if 0%{?rhel} < 7
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}
%endif

## Redefined _pkgdocdir macro for earlier Fedora versions to conform
## this spec with 'F-20 unversioned docdir' change (bz#993984)
%if 0%{?fedora} < 20
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%endif

## Define libraries' destination
%global _incmpidir %{_includedir}/openmpi-%{_arch}
%global _libmpidir %{_libdir}/openmpi/lib

%global soname_version 5.0.0

## Define if use openmpi or not
%global with_openmpi 1

Name: MUMPS
Version: 5.0.1
Release: 4%{?dist}
Summary: A MUltifrontal Massively Parallel sparse direct Solver
License: CeCILL-C 
Group: Development/Libraries
URL: http://mumps.enseeiht.fr/
Source0: http://mumps.enseeiht.fr/%{name}_%{version}.tar.gz

# Custom Makefile changed for Fedora and built from Make.inc/Makefile.gfortran.PAR in the source.
Source1: %{name}-Makefile.par.inc

# Custom Makefile changed for Fedora and built from Make.inc/Makefile.gfortran.SEQ in the source.
Source2: %{name}-Makefile.seq.inc

# These patches create static and shared versions of pord, sequential and mumps libraries
# They are changed for Fedora and  derive from patches for Debian on 
# http://bazaar.launchpad.net/~ubuntu-branches/ubuntu/raring/mumps/raring/files/head:/debian/patches/
Patch0: %{name}-examples-mpilibs.patch
Patch1: %{name}-shared-pord.patch
Patch2: %{name}-shared.patch
Patch3: %{name}-shared-seq.patch

BuildRequires: gcc-gfortran, blas-devel, lapack-devel
BuildRequires: metis-devel, scotch-devel

BuildRequires: openssh-clients
Requires:      %{name}-common = %{version}-%{release}
Requires:      environment-modules 

%description
MUMPS implements a direct solver for large sparse linear systems, with a
particular focus on symmetric positive definite matrices.  It can
operate on distributed matrices e.g. over a cluster.  It has Fortran and
C interfaces, and can interface with ordering tools such as Scotch.

%package devel
Summary: The MUMPS headers and development-related files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
%description devel
Shared links and header files.
This package contains dummy MPI header file 
including symbols used by MUMPS.

%package examples
Summary: The MUMPS common illustrative test programs
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
%description examples
This package contains common illustrative 
test programs about how MUMPS can be used.

%package common
Summary: Documentation files for MUMPS
Group: Development/Libraries
BuildArch: noarch
%description common
This package contains common documentation files for MUMPS.

########################################################
%if 0%{?with_openmpi}
%package openmpi
Summary: MUMPS libraries compiled against openmpi
Group: Development/Libraries

BuildRequires: openmpi-devel
BuildRequires: blacs-openmpi-devel
BuildRequires: scalapack-openmpi-devel
BuildRequires: metis-devel, ptscotch-openmpi-devel

Requires: %{name}-common = %{version}-%{release}
Requires: openmpi
%description openmpi
MUMPS libraries compiled against openmpi

%package openmpi-devel
Summary: The MUMPS headers and development-related files
Group: Development/Libraries
BuildRequires: openmpi-devel
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
%description openmpi-devel
Shared links, header files for MUMPS.
%endif
##########################################################

%prep
%setup -q -n %{name}_%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

mv examples/README examples/README-examples

%build

#######################################################
## Build MPI version
rm -f Makefile.inc
cp -f %{SOURCE1} Makefile.inc

# Set build flags macro
sed -e 's|@@CFLAGS@@|%{optflags} %{__global_ldflags} -Wl,-z,now -Dscotch -Dmetis -Dptscotch|g' -i Makefile.inc
sed -e 's|@@-O@@|%{__global_ldflags} -Wl,-z,now -Wl,--as-needed|g' -i Makefile.inc

## EPEL7 still provides OpenMPI 1.6.4
%if 0%{?epel} >= 7
sed -e 's|@@MPIFORTRANLIB@@|-lmpi_f77|g' -i Makefile.inc
%else
sed -e 's|@@MPIFORTRANLIB@@|-lmpi_mpifh|g' -i Makefile.inc
%endif

MUMPS_MPI=openmpi
MUMPS_INCDIR=-I%{_includedir}/openmpi-%{_arch}
LMETISDIR=%{_libdir}
LMETIS="-L%{_libdir} -lmetis"
SCOTCHDIR=%{_libdir}/openmpi
ISCOTCH=-I%{_includedir}/openmpi-%{_arch}
LSCOTCH="-L%{_libdir}/openmpi/lib -lesmumps -lscotch -lscotcherr -lptesmumps -lptscotch -lptscotcherr"

export MPIBLACSLIBS="-lmpiblacs"

%if 0%{?with_openmpi}
export MPI_COMPILER_NAME=openmpi
%{_openmpi_load}
export LD_LIBRARY_PATH="%{_libdir}/openmpi/lib"
export LDFLAGS="%{__global_ldflags} -Wl,-z,now -Wl,--as-needed"
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/lib
make \
 FC=%{_libdir}/openmpi/bin/mpif77 \
 MUMPS_MPI="$MUMPS_MPI" \
 MUMPS_INCDIR="$MUMPS_INCDIR" \
 MUMPS_LIBF77="-L%{_libdir}/openmpi -L%{_libdir}/openmpi/lib -lmpi $MPIFORTRANSLIB -lscalapack $MPIBLACSLIBS" \
 LMETISDIR="$LMETISDIR" LMETIS="$LMETIS" \
 SCOTCHDIR=$SCOTCHDIR \
 ISCOTCH=$ISCOTCH \
 LSCOTCH="$LSCOTCH" all
%{_openmpi_unload}
cp -pr lib/* %{name}-%{version}-$MPI_COMPILER_NAME/lib
rm -rf lib/*
make clean
%endif

######################################################

patch -p0 < %{PATCH3}

## Build serial version
rm -f Makefile.inc
cp -f %{SOURCE2} Makefile.inc

# Set build flags macro
sed -e 's|@@CFLAGS@@|%{optflags} %{__global_ldflags} -Wl,-z,now -Dscotch -Dmetis|g' -i Makefile.inc
sed -e 's|@@-O@@|%{__global_ldflags} -Wl,-z,now -Wl,--as-needed|g' -i Makefile.inc

export LDFLAGS="%{__global_ldflags} -Wl,-z,now -Wl,--as-needed"
make \
 MUMPS_LIBF77="-L%{_libdir} -lblas -llapack" \
 LIBSEQ="-L../libseq -lmpiseq" \
 INCSEQ="-I../libseq" \
 LMETISDIR=%{_libdir} \
 LMETIS="-L%{_libdir} -lmetis" \
 SCOTCHDIR=%{_prefix} \
 ISCOTCH=-I%{_includedir} \
 LSCOTCH="-L%{_libdir} -lesmumps -lscotch -lscotcherr -lscotchmetis" \
 all
#######################################################

# Make sure documentation is using Unicode.
iconv -f iso8859-1 -t utf-8 README > README-t && mv README-t README

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if 0%{?with_openmpi}
%post openmpi -p /sbin/ldconfig
%postun openmpi -p /sbin/ldconfig
%endif

%check
# Running test programs showing how MUMPS can be used
cd examples

LD_LIBRARY_PATH=$PWD:../lib:$LD_LIBRARY_PATH \
 ./ssimpletest < input_simpletest_real
LD_LIBRARY_PATH=$PWD:../lib:$LD_LIBRARY_PATH \
 ./dsimpletest < input_simpletest_real
LD_LIBRARY_PATH=$PWD:../lib:$LD_LIBRARY_PATH \
 ./csimpletest < input_simpletest_cmplx
LD_LIBRARY_PATH=$PWD:../lib:$LD_LIBRARY_PATH \
 ./zsimpletest < input_simpletest_cmplx
LD_LIBRARY_PATH=$PWD:../lib:$LD_LIBRARY_PATH \
 ./c_example

%if 0%{?with_openmpi}
%if 0%{?rhel}
module load %{_sysconfdir}/modulefiles/openmpi-%{_arch}
%else
%{_openmpi_load}
%endif
LD_LIBRARY_PATH=$PWD:../%{name}-%{version}-openmpi/lib:$LD_LIBRARY_PATH \
 ./ssimpletest < input_simpletest_real
LD_LIBRARY_PATH=$PWD:../%{name}-%{version}-openmpi/lib:$LD_LIBRARY_PATH \
 ./dsimpletest < input_simpletest_real
LD_LIBRARY_PATH=$PWD:../%{name}-%{version}-openmpi/lib:$LD_LIBRARY_PATH \
 ./csimpletest < input_simpletest_cmplx
LD_LIBRARY_PATH=$PWD:../%{name}-%{version}-openmpi/lib:$LD_LIBRARY_PATH \
 ./zsimpletest < input_simpletest_cmplx
LD_LIBRARY_PATH=$PWD:../%{name}-%{version}-openmpi/lib:$LD_LIBRARY_PATH \
 ./c_example
%{_openmpi_unload}
cd ../
%endif

%install

#########################################################
%if 0%{?with_openmpi}
mkdir -p $RPM_BUILD_ROOT%{_libmpidir}
mkdir -p $RPM_BUILD_ROOT%{_libmpidir}/%{name}-%{version}/examples
mkdir -p $RPM_BUILD_ROOT%{_incmpidir}

%{_openmpi_load}
# Install libraries.
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*-*.so $RPM_BUILD_ROOT%{_libmpidir}

# Install development files.
install -cpm 755 %{name}-%{version}-openmpi/lib/libmumps_common.so $RPM_BUILD_ROOT%{_libmpidir}
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*mumps.so $RPM_BUILD_ROOT%{_libmpidir}
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*mumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libmpidir}
install -cpm 755 %{name}-%{version}-openmpi/lib/libpord-%{soname_version}.so $RPM_BUILD_ROOT%{_libmpidir}
install -cpm 755 %{name}-%{version}-openmpi/lib/libpord.so $RPM_BUILD_ROOT%{_libmpidir}

# Make symbolic links instead hard-link 
ln -sf %{_libmpidir}/libsmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libmpidir}/libsmumps.so
ln -sf %{_libmpidir}/libcmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libmpidir}/libcmumps.so
ln -sf %{_libmpidir}/libzmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libmpidir}/libzmumps.so
ln -sf %{_libmpidir}/libdmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libmpidir}/libdmumps.so
ln -sf %{_libmpidir}/libmumps_common-%{soname_version}.so $RPM_BUILD_ROOT%{_libmpidir}/libmumps_common.so
ln -sf %{_libmpidir}/libpord-%{soname_version}.so $RPM_BUILD_ROOT%{_libmpidir}/libpord.so

install -cpm 644 include/*.h $RPM_BUILD_ROOT%{_incmpidir}
%{_openmpi_unload}
%endif
##########################################################

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}

# Install libraries.
install -cpm 755 lib/lib*-*.so $RPM_BUILD_ROOT%{_libdir}

# Install development files.
install -cpm 755 lib/libmumps_common.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 lib/lib*mumps.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 lib/lib*mumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 lib/libpord-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 lib/libpord.so $RPM_BUILD_ROOT%{_libdir}

# Make symbolic links instead hard-link 
ln -sf %{_libdir}/libsmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libsmumps.so
ln -sf %{_libdir}/libcmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libcmumps.so
ln -sf %{_libdir}/libzmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libzmumps.so
ln -sf %{_libdir}/libdmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libdmumps.so
ln -sf %{_libdir}/libmumps_common-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libmumps_common.so
ln -sf %{_libdir}/libpord-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libpord.so

install -cpm 644 include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -cpm 644 libseq/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}

install -cpm 755 examples/?simpletest $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
install -cpm 755 examples/input_* $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
install -cpm 644 examples/README-examples $RPM_BUILD_ROOT%{_pkgdocdir}
install -cpm 644 doc/*.pdf $RPM_BUILD_ROOT%{_pkgdocdir}
install -cpm 644 ChangeLog LICENSE README $RPM_BUILD_ROOT%{_pkgdocdir}

#######################################################
%if 0%{?with_openmpi}
%files openmpi
%{_libmpidir}/libpord-%{soname_version}.so
%{_libmpidir}/lib?mumps-%{soname_version}.so
%{_libmpidir}/libmumps_common-%{soname_version}.so

%files openmpi-devel
%{_incmpidir}/*.h
%{_libmpidir}/lib?mumps.so
%{_libmpidir}/libmumps_common.so
%{_libmpidir}/libpord.so
%endif
#######################################################

%files
%{_libdir}/libpord-%{soname_version}.so
%{_libdir}/lib?mumps-%{soname_version}.so
%{_libdir}/libmumps_common-%{soname_version}.so

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/lib?mumps.so
%{_libdir}/libmumps_common.so
%{_libdir}/libpord.so

%files common
## This directory contains README*, LICENSE, ChangeLog, UserGuide files
%{_pkgdocdir}/
%if 0%{?fedora}
%license %{_pkgdocdir}/LICENSE
%endif

%files examples
%dir %{_libexecdir}/%{name}-%{version}
%{_libexecdir}/%{name}-%{version}/examples/

%changelog
* Fri Oct 30 2015 Antonio Trande <sagitterATfedoraproject.org> - 5.0.1-4
- Hardened builds on <F23

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 5.0.1-3
- Rebuild for openmpi 1.10.0

* Sun Jul 26 2015 Sandro Mani <manisandro@gmail.com> - 5.0.1-2
- Rebuild for RPM MPI Requires Provides Change

* Fri Jul 24 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1
- Added a soname_version macro

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 25 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.0-2
- Fixed conditional macro for OpenMPI sub-package on EPEL7
- Fixed library linkage against OpenMPI on EPEL7
- Added ORDERINGSF variables for Scotch and Metis

* Fri Feb 20 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.0-1
- Update to MUMPS-5.0.0
- License changed in CeCILL-C
- Linked against Metis
- Linked serial version against Scotch
- Linked MPI version against PT-Scotch

* Mon Nov 10 2014 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-24
- Removed OpenMPI minimal release request for EPEL
- Fixed scalapack minimal release request

* Mon Oct 27 2014 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-23
- Rebuild after scalapack-2.0.2-5.el6.1 update (bz#1157775)

* Tue Sep 23 2014 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-22 
- MUMPS-openmpi linked to 'lapack' libs in the EPEL6 buildings

* Sun Sep 07 2014 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-21 
- Changed MUMPS sequential build setups
- Packaged dummy mpif.h file including symbols used by MUMPS

* Mon Aug 25 2014 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-20 
- Excluded Fortran driver tests

* Sat Aug 23 2014 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-19 
- Fixed BR for OpenMPI sub-packages
- Performed serial and parallel MUMPS tests

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-18 
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-17
- Some MPI packaging fixes
- Changed MUMPS sequential build

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May  3 2014 Tom Callaway <spot@fedoraproject.org> - 4.10.0-15
- rebuild against new scalapack tree of blacs

* Wed Aug 28 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-14
- 'blacs-openmpi-devel' request unversioned
- Defined which version of MUMPS-doc package is obsolete

* Wed Aug 07 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-13
- Obsolete packages are now versioned (bz#993574)
- Adding redefined _pkgdocdir macro for earlier Fedora versions to conform
  this spec with 'F-20 unversioned docdir' change (bz#993984)

* Mon Jul 29 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-12
- Old MUMPS subpackages are now obsoletes

* Sat Jul 27 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-11
- Added new macros for 'openmpi' destination directories
- Done some package modifications according to MPI guidelines
- This .spec file now produces '-openmpi', '-openmpi-devel', '-common' packages
- Added MUMPS packaging in "serial mode"
- %%{name}-common package is a noarch
- Added an '-examples' subpackage that contains all test programs

* Tue Jul 23 2013 Antonio Trande <sagitter@fedoraproject.org> - 4.10.0-10
- 'openmpi-devel' BR changed to 'openmpi-devel>=1.7'
- 'blacs-openmpi-devel' BR changed to 'blacs-openmpi-devel>=1.1-50'
- Removed '-lmpi_f77' library link, deprecated starting from 'openmpi-1.7.2'

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
