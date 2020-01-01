## Define libraries' destination
%global _incmpidir %{_includedir}/openmpi-%{_arch}
%global _libmpidir %{_libdir}/openmpi/lib
%global _incmpichdir %{_includedir}/mpich-%{_arch}
%global _libmpichdir %{_libdir}/mpich/lib

%global soname_version 5.2

%undefine _ld_as_needed

%ifarch %{openblas_arches}
%global with_openmp 1
%else
%global with_openmp 0
%endif

%if 0%{?rhel} || 0%{?rhel} >= 7
%global with_mpicheck 1
%global with_mpich 1
%global with_openmpi 1
%endif

%global with_mpich 1
%global with_openmpi 1

Name: MUMPS
Version: 5.2.1
Release: 4%{?dist}
Summary: A MUltifrontal Massively Parallel sparse direct Solver
License: CeCILL-C 
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

Patch4: %{name}-shared-pord-openmp.patch
Patch5: %{name}-shared-openmp.patch
Patch6: %{name}-shared-seq-openmp.patch
Patch7: %{name}-examples-openmp.patch

BuildRequires: gcc-gfortran
%ifarch %{openblas_arches}
BuildRequires: openblas-devel, openblas-srpm-macros
%else
BuildRequires: blas-devel
BuildRequires: lapack-devel
%endif
BuildRequires: metis-devel
BuildRequires: scotch-devel

BuildRequires: openssh-clients
BuildRequires: hwloc-devel
Requires:      %{name}-common = %{version}-%{release}

%description
MUMPS implements a direct solver for large sparse linear systems, with a
particular focus on symmetric positive definite matrices.  It can
operate on distributed matrices e.g. over a cluster.  It has Fortran and
C interfaces, and can interface with ordering tools such as Scotch.

%package devel
Summary: The MUMPS headers and development-related files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran%{?_isa}
%description devel
Shared links and header files.
This package contains dummy MPI header file 
including symbols used by MUMPS.

%package examples
Summary: The MUMPS common illustrative test programs
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
This package contains common illustrative
test programs about how MUMPS can be used.

%package common
Summary: Documentation files for MUMPS
BuildArch: noarch
%description common
This package contains common documentation files for MUMPS.

########################################################
%if 0%{?with_openmp}
%package openmp
Summary: MUMPS libraries with OpenMP support

%ifarch %{openblas_arches}
BuildRequires: openblas-devel, openblas-srpm-macros
%else
BuildRequires: blas-devel
BuildRequires: lapack-devel
%endif
Requires: %{name}-common = %{version}-%{release}
%description openmp
MUMPS libraries with OpenMP support.

%package openmp-devel
Summary: The MUMPS headers and development-related files
Requires: %{name}-openmp%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description openmp-devel
Shared links, header files for MUMPS OpenMP.

%package openmp-examples
Summary: The MUMPS OpenMP common illustrative test programs
Requires: %{name}-openmp%{?_isa} = %{version}-%{release}
%description openmp-examples
This package contains common illustrative
test programs about how MUMPS-openmp can be used.
%endif
##########################################################

########################################################
%if 0%{?with_openmpi}
%package openmpi
Summary: MUMPS libraries compiled against openmpi

BuildRequires: openmpi-devel
BuildRequires: blacs-openmpi-devel
BuildRequires: scalapack-openmpi-devel
BuildRequires: metis-devel, ptscotch-openmpi-devel
%if 0%{?fedora}
BuildRequires: rpm-mpi-hooks
%endif
Requires: %{name}-common = %{version}-%{release}
Requires: openmpi%{?_isa}
Requires: scalapack-openmpi%{?_isa}

%description openmpi
MUMPS libraries compiled against openmpi.

%package openmpi-devel
Summary: The MUMPS headers and development-related files
BuildRequires: openmpi-devel
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran%{?_isa}
%if 0%{?fedora}
Requires: rpm-mpi-hooks
%endif
%description openmpi-devel
Shared links, header files for MUMPS.

%package openmpi-examples
Summary: The MUMPS OpenMPI common illustrative test programs
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: openmpi
%if 0%{?fedora}
BuildRequires: rpm-mpi-hooks
%endif

%description openmpi-examples
This package contains common illustrative
test programs about how MUMPS-openmpi can be used.
%endif
##########################################################

########################################################
%if 0%{?with_mpich}
%package mpich
Summary: MUMPS libraries compiled against MPICH

BuildRequires: mpich-devel
BuildRequires: blacs-mpich-devel
BuildRequires: scalapack-mpich-devel
BuildRequires: metis-devel, ptscotch-mpich-devel
%if 0%{?fedora}
BuildRequires: rpm-mpi-hooks
%endif
Requires: %{name}-common = %{version}-%{release}
Requires: mpich%{?_isa}
Requires: scalapack-mpich%{?_isa}

%description mpich
MUMPS libraries compiled against MPICH.

%package mpich-devel
Summary: The MUMPS headers and development-related files
BuildRequires: mpich-devel
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
%if 0%{?fedora}
Requires: rpm-mpi-hooks
%endif
%description mpich-devel
Shared links, header files for MUMPS.

%package mpich-examples
Summary: The MUMPS MPICH common illustrative test programs
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: gcc-gfortran%{?_isa}
Requires: mpich
%if 0%{?fedora}
BuildRequires: rpm-mpi-hooks
%endif
%description mpich-examples
This package contains common illustrative
test programs about how MUMPS-mpich can be used.
%endif
##########################################################

%prep
%setup -q -n %{name}_%{version}

%patch0 -p1 -b .examples-mpilibs
%patch1 -p1 -b .shared-pord
%patch2 -p1 -b .shared

mv examples/README examples/README-examples

%build

#######################################################
## Build MPI version
rm -f Makefile.inc
%if 0%{?with_openmpi}
%{_openmpi_load}
cp -f %{SOURCE1} Makefile.inc

# -DBLR_MT needs OpenMP
sed -e 's| -DBLR_MT||g' -i Makefile.inc

%if 0%{?fedora}
%global mpif77_cflags %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --cflags ompi-f77)
%global mpif77_libs %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --libs ompi-f77)
%global mpifort_cflags %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --cflags ompi-fort)
%global mpifort_libs %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --libs ompi-fort)
%global mpic_libs %(env PKG_CONFIG_PATH=%{_libmpidir}/pkgconfig pkg-config --libs ompi)
%endif
%if 0%{?rhel}
%global mpif77_cflags -I%{_incmpidir}
%global mpif77_libs -lmpi_mpifh
%global mpifort_cflags -I%{_incmpidir}
%global mpifort_libs -lmpi_mpifh
%global mpic_libs -lmpi
%endif

# Set build flags macro
sed -e 's|@@CFLAGS@@|%{optflags} -Dscotch -Dmetis -Dptscotch -DWITHOUT_PTHREAD -I${MPI_FORTRAN_MOD_DIR}|g' -i Makefile.inc
sed -e 's|@@-O@@|%{__global_ldflags}|g' -i Makefile.inc
sed -e 's|@@MPICLIB@@|-lmpi|g' -i Makefile.inc

%if 0%{?rhel} && 0%{?rhel} >= 7
sed -e 's|@@MPIFORTRANLIB@@|-L%{_libmpidir} -Wl,-rpath -Wl,%{_libmpidir} %{mpif77_libs}|g' -i Makefile.inc
%endif

%if 0%{?fedora}
sed -e 's|@@MPIFORTRANLIB@@|%{mpifort_libs}|g' -i Makefile.inc
%endif

MUMPS_MPI=openmpi
MUMPS_INCDIR=-I$MPI_INCLUDE
LMETISDIR=%{_libdir}
LMETIS="-L%{_libdir} -lmetis"
SCOTCHDIR=$MPI_LIB
ISCOTCH=-I$MPI_INCLUDE
LSCOTCH=" -L$MPI_LIB -lesmumps -lscotch -lscotcherr -lptesmumps -lptscotch -lptscotcherr"
IPORD=" -I$PWD/PORD/include/"
LPORD=" -L$PWD/PORD/lib -lpord"

%if 0%{?rhel} && 0%{?rhel} >= 7
export MPIBLACSLIBS="-L$MPI_LIB -lmpiblacs"
%endif
export MPI_COMPILER_NAME=openmpi
export LD_LIBRARY_PATH="$MPI_LIB:%{_libdir}"
export LDFLAGS="%{__global_ldflags}"

mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/lib
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/examples
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/modules

%ifarch %{openblas_arches}
export LIBBLAS="-L%{_libdir} -lopenblas"
export INCBLAS=-I%{_includedir}/openblas
%else
export LIBBLAS="-L%{_libdir} -lblas -llapack"
export INCBLAS=-I%{_includedir}
%endif

make all \
 SONAME_VERSION=%{soname_version} \
 CC=$MPI_BIN/mpicc \
 FC=$MPI_BIN/mpif77 \
 FL=$MPI_BIN/mpif77 \
 MUMPS_MPI="$MUMPS_MPI" \
 MUMPS_INCDIR="$MUMPS_INCDIR $INCBLAS" \
 MUMPS_LIBF77="${LIBBLAS} -L$MPI_LIB -Wl,-rpath -Wl,$MPI_LIB %{mpic_libs} $MPIFORTRANSLIB -lscalapack %{?rhel:$MPIBLACSLIBS}" \
 LMETISDIR="$LMETISDIR" LMETIS="$LMETIS" \
 SCOTCHDIR=$SCOTCHDIR \
 ISCOTCH=$ISCOTCH \
 LSCOTCH="$LSCOTCH" \
 IPORD="$IPORD" \
 LPORD="$LPORD" \
 OPTL="%{__global_ldflags}"
%{_openmpi_unload}
cp -pr lib/* %{name}-%{version}-$MPI_COMPILER_NAME/lib
cp -pr examples/* %{name}-%{version}-$MPI_COMPILER_NAME/examples
rm -rf lib/*
cp -pr src/*.mod %{name}-%{version}-$MPI_COMPILER_NAME/modules
make clean
%endif

######################################################
#######################################################
## Build MPICH version
%if 0%{?with_mpich}
rm -f Makefile.inc
cp -f %{SOURCE1} Makefile.inc

# -DBLR_MT needs OpenMP
sed -e 's| -DBLR_MT||g' -i Makefile.inc

%{_mpich_load}
%global mpif77_cflags %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --cflags mpich)
%global mpif77_libs %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --libs mpich)
%global mpifort_cflags %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --cflags mpich)
%global mpifort_libs %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --libs mpich)
%global mpich_libs %(env PKG_CONFIG_PATH=%{_libmpichdir}/pkgconfig pkg-config --libs mpich)

# Set build flags macro
sed -e 's|@@CFLAGS@@|%{optflags} -Dscotch -Dmetis -Dptscotch -DWITHOUT_PTHREAD -I${MPI_FORTRAN_MOD_DIR}|g' -i Makefile.inc
sed -e 's|@@-O@@|%{__global_ldflags}|g' -i Makefile.inc
sed -e 's|@@MPICLIB@@|-lmpich|g' -i Makefile.inc
sed -e 's|@@MPIFORTRANLIB@@|%{mpifort_libs}|g' -i Makefile.inc

MUMPS_MPI=mpich
MUMPS_INCDIR=-I$MPI_INCLUDE
LMETISDIR=%{_libdir}
LMETIS="-L%{_libdir} -lmetis"
SCOTCHDIR=$MPI_LIB
ISCOTCH=-I$MPI_INCLUDE
LSCOTCH=" -L$MPI_LIB -lesmumps -lscotch -lscotcherr -lptesmumps -lptscotch -lptscotcherr"
export IPORD=" -I$PWD/PORD/include/"
export LPORD=" -L$PWD/PORD/lib -lpord"

%if 0%{?rhel} && 0%{?rhel} >= 7
export MPIBLACSLIBS="-L$MPI_LIB -lmpiblacs"
%endif
export MPI_COMPILER_NAME=mpich
export LD_LIBRARY_PATH=$MPI_LIB:%{_libdir}
export LDFLAGS="%{__global_ldflags}"

mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/lib
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/examples
mkdir -p %{name}-%{version}-$MPI_COMPILER_NAME/modules

%ifarch %{openblas_arches}
export LIBBLAS="-L%{_libdir} -lopenblas"
export INCBLAS=-I%{_includedir}/openblas
%else
export LIBBLAS="-L%{_libdir} -lblas -llapack"
export INCBLAS=-I%{_includedir}
%endif

make all \
 SONAME_VERSION=%{soname_version} \
 CC=$MPI_BIN/mpicc \
 FC=$MPI_BIN/mpif77 \
 FL=$MPI_BIN/mpif77 \
 MUMPS_MPI="$MUMPS_MPI" \
 MUMPS_INCDIR="$MUMPS_INCDIR $INCBLAS" \
 MUMPS_LIBF77="${LIBBLAS} -L$MPI_LIB %{mpich_libs} $MPIFORTRANSLIB -lscalapack %{?rhel:$MPIBLACSLIBS}" \
 LMETISDIR="$LMETISDIR" LMETIS="$LMETIS" \
 SCOTCHDIR=$SCOTCHDIR \
 ISCOTCH=$ISCOTCH \
 LSCOTCH="$LSCOTCH" \
 IPORD="$IPORD" \
 LPORD="$LPORD" \
 OPTL="%{__global_ldflags}"
%{_mpich_unload}
cp -pr lib/* %{name}-%{version}-$MPI_COMPILER_NAME/lib
cp -pr examples/* %{name}-%{version}-$MPI_COMPILER_NAME/examples
rm -rf lib/*
cp -pr src/*.mod %{name}-%{version}-$MPI_COMPILER_NAME/modules
make clean
%endif

######################################################

patch -p0 < %{PATCH3}

## Build serial version
rm -f Makefile.inc
cp -f %{SOURCE2} Makefile.inc

# -DBLR_MT needs OpenMP
sed -e 's| -DBLR_MT||g' -i Makefile.inc

# Set build flags macro
sed -e 's|@@CFLAGS@@|%{optflags} -Dscotch -Dmetis -DWITHOUT_PTHREAD -I%{_fmoddir}|g' -i Makefile.inc
sed -e 's|@@-O@@|%{__global_ldflags}|g' -i Makefile.inc

mkdir -p %{name}-%{version}/lib
mkdir -p %{name}-%{version}/examples
mkdir -p %{name}-%{version}/modules

IPORD=" -I$PWD/PORD/include/"
LPORD=" -L$PWD/PORD/lib -lpord"

%ifarch %{openblas_arches}
export LIBBLAS="-L%{_libdir} -lopenblas"
export INCBLAS=-I%{_includedir}/openblas
%else
export LIBBLAS="-L%{_libdir} -lblas -llapack"
export INCBLAS=-I%{_includedir}
%endif

export LDFLAGS="%{__global_ldflags} -Wl,-z,now"
make all \
 SONAME_VERSION=%{soname_version} \
 CC=gcc \
 FC=gfortran \
 FL=gfortran \
 MUMPS_LIBF77="${LIBBLAS}" \
 LIBBLAS="${LIBBLAS}" \
 LIBOTHERS=" -lpthread" \
 LIBSEQ="-L../libseq -lmpiseq" \
 INCSEQ="-I../libseq $INCBLAS" \
 LMETISDIR=%{_libdir} \
 LMETIS="-L%{_libdir} -lmetis" \
 SCOTCHDIR=%{_prefix} \
 ISCOTCH=-I%{_includedir} \
 LSCOTCH=" -L%{_libdir} -lesmumps -lscotch -lscotcherr -lscotchmetis" \
 IPORD="$IPORD" \
 LPORD="$LPORD" \
 OPTL="%{__global_ldflags}"
make -C examples
cp -pr lib/* %{name}-%{version}/lib
cp -pr examples/* %{name}-%{version}/examples
rm -rf lib/*
cp -pr src/*.mod %{name}-%{version}/modules
make clean
#######################################################

## Build OpenMP version
%if 0%{?with_openmp}

patch -R -p0 < %{PATCH3}
patch -R -p1 < %{PATCH2}
patch -R -p1 < %{PATCH1}

patch -p1 < %{PATCH4}
patch -p1 < %{PATCH5}
patch -p0 < %{PATCH6}
patch -p0 < %{PATCH7}

rm -f Makefile.inc
cp -f %{SOURCE2} Makefile.inc

# Set build flags macro
sed -e 's|@@CFLAGS@@|%{optflags} -fopenmp -Dscotch -Dmetis -DWITHOUT_PTHREAD -I%{_fmoddir}|g' -i Makefile.inc
sed -e 's|@@-O@@|%{__global_ldflags} -fopenmp -lgomp -lrt|g' -i Makefile.inc

mkdir -p %{name}-%{version}-openmp/lib
mkdir -p %{name}-%{version}-openmp/examples
mkdir -p %{name}-%{version}-openmp/modules

IPORD=" -I$PWD/PORD/include/"
LPORD=" -L$PWD/PORD/lib -lpordo"

%ifarch %{openblas_arches}
export LIBBLAS="-L%{_libdir} -lopenblaso"
export INCBLAS=-I%{_includedir}/openblas
%else
export LIBBLAS="-L%{_libdir} -lblas -llapack"
export INCBLAS=-I%{_includedir}
%endif

export LDFLAGS="%{__global_ldflags} -fopenmp -lgomp -lrt"
make all \
 SONAME_VERSION=%{soname_version} \
 CC=gcc \
 FC=gfortran \
 FL=gfortran \
 MUMPS_LIBF77="${LIBBLAS}" \
 LIBBLAS="${LIBBLAS}" \
 LIBOTHERS=" " \
 LIBSEQ="-L../libseq -lmpiseqo" \
 INCSEQ="-I../libseq $INCBLAS" \
 LMETISDIR=%{_libdir} \
 LMETIS="-L%{_libdir} -lmetis" \
 SCOTCHDIR=%{_prefix} \
 ISCOTCH="-I%{_includedir}" \
 LSCOTCH=" -L%{_libdir} -lesmumps -lscotch -lscotcherr -lscotchmetis" \
 IPORD="$IPORD" \
 LPORD="$LPORD" \
 OPTL="%{__global_ldflags} -fopenmp -lrt"
make -C examples
cp -pr lib/* %{name}-%{version}-openmp/lib
cp -pr examples/* %{name}-%{version}-openmp/examples
rm -rf lib/*
cp -pr src/*.mod %{name}-%{version}-openmp/modules
make clean
%endif
#######################################################

# Make sure documentation is using Unicode.
iconv -f iso8859-1 -t utf-8 README > README-t && mv README-t README

%ldconfig_scriptlets

%if 0%{?with_openmp}
%ldconfig_scriptlets openmp
%endif

%check
# Running test programs
pushd %{name}-%{version}/examples
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
popd

%if 0%{?with_openmp}
pushd %{name}-%{version}-openmp/examples
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
popd
%endif

%if 0%{?with_mpicheck}
%if 0%{?with_openmpi}
%{_openmpi_load}
pushd %{name}-%{version}-openmpi/examples
export LD_LIBRARY_PATH=$PWD:../lib:$LD_LIBRARY_PATH
# Allow openmpi to run with more processes than cores
export OMPI_MCA_rmaps_base_oversubscribe=1
./ssimpletest < input_simpletest_real
./dsimpletest < input_simpletest_real
./csimpletest < input_simpletest_cmplx
./zsimpletest < input_simpletest_cmplx
mpirun -np 3 ./c_example
popd
%{_openmpi_unload}
%endif

%if 0%{?with_mpich}
## Tests not perfomred due to 'gethostname' failure on koji
%endif
%endif

%install

#########################################################
%if 0%{?with_openmpi}
%{_openmpi_load}
mkdir -p $RPM_BUILD_ROOT$MPI_LIB
mkdir -p $RPM_BUILD_ROOT%{_libdir}/openmpi/%{name}-%{version}-examples
mkdir -p $RPM_BUILD_ROOT$MPI_INCLUDE
mkdir -p $RPM_BUILD_ROOT$MPI_FORTRAN_MOD_DIR/%{name}-%{version}

# Install libraries.
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*-*.so $RPM_BUILD_ROOT$MPI_LIB

# Install development files.
install -cpm 755 %{name}-%{version}-openmpi/lib/libmumps_common.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*mumps.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-openmpi/lib/lib*mumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-openmpi/lib/libpord-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-openmpi/lib/libpord.so $RPM_BUILD_ROOT$MPI_LIB

# Make symbolic links instead hard-link 
ln -sf $MPI_LIB/libsmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libsmumps.so
ln -sf $MPI_LIB/libcmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libcmumps.so
ln -sf $MPI_LIB/libzmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libzmumps.so
ln -sf $MPI_LIB/libdmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libdmumps.so
ln -sf $MPI_LIB/libmumps_common-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libmumps_common.so
ln -sf $MPI_LIB/libpord-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libpord.so

install -cpm 755 %{name}-%{version}-openmpi/examples/?simpletest $RPM_BUILD_ROOT%{_libdir}/openmpi/%{name}-%{version}-examples
install -cpm 755 %{name}-%{version}-openmpi/examples/input_* $RPM_BUILD_ROOT%{_libdir}/openmpi/%{name}-%{version}-examples
install -cpm 755 %{name}-%{version}-openmpi/examples/README-* $RPM_BUILD_ROOT%{_libdir}/openmpi/%{name}-%{version}-examples

install -cpm 644 include/*.h $RPM_BUILD_ROOT$MPI_INCLUDE
install -cpm 644 PORD/include/* $RPM_BUILD_ROOT$MPI_INCLUDE
install -cpm 644 %{name}-%{version}-openmpi/modules/* $RPM_BUILD_ROOT$MPI_FORTRAN_MOD_DIR/%{name}-%{version}/
%{_openmpi_unload}
%endif
##########################################################

#########################################################
%if 0%{?with_mpich}
%{_mpich_load}
mkdir -p $RPM_BUILD_ROOT$MPI_LIB
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mpich/%{name}-%{version}-examples
mkdir -p $RPM_BUILD_ROOT$MPI_INCLUDE
mkdir -p $RPM_BUILD_ROOT$MPI_FORTRAN_MOD_DIR/%{name}-%{version}

# Install libraries.
install -cpm 755 %{name}-%{version}-mpich/lib/lib*-*.so $RPM_BUILD_ROOT$MPI_LIB

# Install development files.
install -cpm 755 %{name}-%{version}-mpich/lib/libmumps_common.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-mpich/lib/lib*mumps.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-mpich/lib/lib*mumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-mpich/lib/libpord-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB
install -cpm 755 %{name}-%{version}-mpich/lib/libpord.so $RPM_BUILD_ROOT$MPI_LIB

# Make symbolic links instead hard-link 
ln -sf $MPI_LIB/libsmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libsmumps.so
ln -sf $MPI_LIB/libcmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libcmumps.so
ln -sf $MPI_LIB/libzmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libzmumps.so
ln -sf $MPI_LIB/libdmumps-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libdmumps.so
ln -sf $MPI_LIB/libmumps_common-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libmumps_common.so
ln -sf $MPI_LIB/libpord-%{soname_version}.so $RPM_BUILD_ROOT$MPI_LIB/libpord.so

install -cpm 755 %{name}-%{version}-mpich/examples/?simpletest $RPM_BUILD_ROOT%{_libdir}/mpich/%{name}-%{version}-examples
install -cpm 755 %{name}-%{version}-mpich/examples/input_* $RPM_BUILD_ROOT%{_libdir}/mpich/%{name}-%{version}-examples
install -cpm 755 %{name}-%{version}-mpich/examples/README-* $RPM_BUILD_ROOT%{_libdir}/mpich/%{name}-%{version}-examples

install -cpm 644 include/*.h $RPM_BUILD_ROOT$MPI_INCLUDE
install -cpm 644 PORD/include/* $RPM_BUILD_ROOT$MPI_INCLUDE
install -cpm 644 %{name}-%{version}-mpich/modules/* $RPM_BUILD_ROOT$MPI_FORTRAN_MOD_DIR/%{name}-%{version}/
%{_mpich_unload}
%endif
##########################################################

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_fmoddir}/%{name}-%{version}

# Install libraries.
install -cpm 755 %{name}-%{version}/lib/lib*-*.so $RPM_BUILD_ROOT%{_libdir}

# Install development files.
install -cpm 755 %{name}-%{version}/lib/libmumps_common.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}/lib/lib*mumps.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}/lib/lib*mumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}/lib/libpord-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}/lib/libpord.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}/lib/libmpiseq-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}/lib/libmpiseq.so $RPM_BUILD_ROOT%{_libdir}

# Make symbolic links instead hard-link 
ln -sf %{_libdir}/libsmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libsmumps.so
ln -sf %{_libdir}/libcmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libcmumps.so
ln -sf %{_libdir}/libzmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libzmumps.so
ln -sf %{_libdir}/libdmumps-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libdmumps.so
ln -sf %{_libdir}/libmumps_common-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libmumps_common.so
ln -sf %{_libdir}/libpord-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libpord.so
ln -sf %{_libdir}/libmpiseq-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libmpiseq.so

install -cpm 755 %{name}-%{version}/examples/?simpletest $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
install -cpm 755 %{name}-%{version}/examples/input_* $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
install -cpm 755 %{name}-%{version}/examples/README-* $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}/examples
install -cpm 644 %{name}-%{version}/modules/* $RPM_BUILD_ROOT%{_fmoddir}/%{name}-%{version}/

############################################################
%if 0%{?with_openmp}
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}-openmp/examples
mkdir -p $RPM_BUILD_ROOT%{_fmoddir}/%{name}-openmp-%{version}

# Install libraries.
install -cpm 755 %{name}-%{version}-openmp/lib/lib*-*.so $RPM_BUILD_ROOT%{_libdir}

# Install development files.
install -cpm 755 %{name}-%{version}-openmp/lib/libmumpso_common.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}-openmp/lib/lib*mumpso.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}-openmp/lib/lib*mumpso-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}-openmp/lib/libpordo-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}-openmp/lib/libpordo.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}-openmp/lib/libmpiseqo-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}
install -cpm 755 %{name}-%{version}-openmp/lib/libpordo.so $RPM_BUILD_ROOT%{_libdir}

# Make symbolic links instead hard-link 
ln -sf %{_libdir}/libsmumpso-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libsmumpso.so
ln -sf %{_libdir}/libcmumpso-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libcmumpso.so
ln -sf %{_libdir}/libzmumpso-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libzmumpso.so
ln -sf %{_libdir}/libdmumpso-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libdmumpso.so
ln -sf %{_libdir}/libmumpso_common-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libmumpso_common.so
ln -sf %{_libdir}/libpordo-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libpordo.so
ln -sf %{_libdir}/libmpiseqo-%{soname_version}.so $RPM_BUILD_ROOT%{_libdir}/libmpiseqo.so

install -cpm 755 %{name}-%{version}-openmp/examples/?simpletest $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}-openmp/examples
install -cpm 755 %{name}-%{version}-openmp/examples/input_* $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}-openmp/examples
install -cpm 755 %{name}-%{version}-openmp/examples/README-* $RPM_BUILD_ROOT%{_libexecdir}/%{name}-%{version}-openmp/examples
install -cpm 644 %{name}-%{version}-openmp/modules/* $RPM_BUILD_ROOT%{_fmoddir}/%{name}-openmp-%{version}/
%endif
##############################################################

install -cpm 644 include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -cpm 644 libseq/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -cpm 644 PORD/include/* $RPM_BUILD_ROOT%{_includedir}/%{name}

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
%{_fmoddir}/openmpi%{?el7:-%_arch}/%{name}-%{version}/

%files openmpi-examples
%{_libdir}/openmpi/%{name}-%{version}-examples/
%endif
#######################################################

#######################################################
%if 0%{?with_mpich}
%files mpich
%{_libmpichdir}/libpord-%{soname_version}.so
%{_libmpichdir}/lib?mumps-%{soname_version}.so
%{_libmpichdir}/libmumps_common-%{soname_version}.so

%files mpich-devel
%{_incmpichdir}/*.h
%{_libmpichdir}/lib?mumps.so
%{_libmpichdir}/libmumps_common.so
%{_libmpichdir}/libpord.so
%{_fmoddir}/mpich%{?el7:-%_arch}/%{name}-%{version}/

%files mpich-examples
%{_libdir}/mpich/%{name}-%{version}-examples/
%endif
#######################################################

%files
%{_libdir}/libpord-%{soname_version}.so
%{_libdir}/libmpiseq-%{soname_version}.so
%{_libdir}/lib?mumps-%{soname_version}.so
%{_libdir}/libmumps_common-%{soname_version}.so

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_fmoddir}/%{name}-%{version}/
%{_libdir}/lib?mumps.so
%{_libdir}/libmumps_common.so
%{_libdir}/libpord.so
%{_libdir}/libmpiseq.so

%files examples
%{_libexecdir}/%{name}-%{version}/

#######################################################
%if 0%{?with_openmp}
%files openmp
%{_libdir}/libmpiseqo-%{soname_version}.so
%{_libdir}/libpordo-%{soname_version}.so
%{_libdir}/lib?mumpso-%{soname_version}.so
%{_libdir}/libmumpso_common-%{soname_version}.so

%files openmp-devel
%{_libdir}/lib?mumpso.so
%{_libdir}/libmumpso_common.so
%{_libdir}/libpordo.so
%{_libdir}/libmpiseqo.so
%{_fmoddir}/%{name}-openmp-%{version}/

%files openmp-examples
%{_libexecdir}/%{name}-%{version}-openmp/
%endif
#######################################################

%files common
%{!?_licensedir:%global license %doc}
%doc doc/*.pdf ChangeLog README
%license LICENSE

%changelog
* Wed Jan 01 2020 Antonio Trande <sagitter@fedoraproject.org> - 5.2.1-4
- Use libmpiblacs separately on EPEL 7+

* Sun Nov 17 2019 Tom Callaway <spot@fedoraproject.org> - 5.2.1-3
- libmpiblacs is now inside of libscalapack

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 Antonio Trande <sagitter@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Fri May 17 2019 Antonio Trande <sagitter@fedoraproject.org> - 5.1.2-10
- Require scalapack explicity (rhbz #1711291 #1711289)
- Disable tests with OpenMPI-4

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 5.1.2-9
- Rebuild for openmpi 3.1.3

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 19 2018 Sandro Mani <manisandro@gmail.com> - 5.1.2-7
- Rebuild (scotch)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 15 2018 Antonio Trande <sagitter@fedoraproject.org> - 5.1.2-5
- Use %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Antonio Trande <sagitter@fedoraproject.org> - 5.1.2-3
- Rebuild for GCC-8

* Sat Oct 28 2017 Antonio Trande <sagitter@fedoraproject.org> - 5.1.2-2
- Set openblas arches

* Sat Oct 28 2017 Antonio Trande <sagitter@fedoraproject.org> - 5.1.2-1
- Update to 5.1.2
- Add -Wno-unused-dummy-argument -Wno-maybe-uninitialized options
- Add new -DBLR_MT flag
- Rebuild against openblas

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Antonio Trande <sagitter@fedoraproject.org> - 5.1.1-2
- Generate and install libmpiseq libraries (bug fix)

* Tue Mar 21 2017 Antonio Trande <sagitter@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1
- Build openmp version on Fedora and Rhel7 only

* Wed Mar 15 2017 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-9
- Build with openblas on all available architectures

* Tue Feb 14 2017 Antonio Trande <sagitter@fedoraproject.org>  5.0.2-8
- Build OpenMPI version on Fedora26-s390

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Antonio Trande <sagitter@fedoraproject.org>  5.0.2-6
- Rebuild for gcc-gfortran
- Include Fortran modules

* Fri Dec 02 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.2-5
- Fix MPICH builds on s390

* Tue Nov 01 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.2-4
- Build on s390
- Rebuild on epel

* Mon Oct 31 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.2-3
- New architectures

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-2
- Rebuild for openmpi 2.0

* Mon Jul 18 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2

* Fri Apr 29 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-20
- Build MPICH libraries on PPC64* except EPEL6

* Mon Apr 04 2016 Peter Robinson <pbrobinson@fedoraproject.org> - 5.0.1-19
- aarch64/Power64 have mpich/openmpi now

* Wed Mar 23 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-18
- Examples directory moved under /usr/lib/openmpi(mpich)

* Wed Mar 23 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-17
- Added rpm-mpi-hooks as BR in examples sub-packages
- Added openmpi/mpich as Requires package

* Wed Mar 23 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-16
- Added rpm-mpi-hooks dependencies

* Wed Mar 23 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-15
- Fixed linker flags

* Tue Mar 22 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-14
- Fixed MPI paths

* Sun Mar 20 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-13
- Rebuild for Metis
- Compiled with OpenMP support (bz#1319477)

* Fri Feb 12 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-12
- Added linker flags to fix unused-direct-shlib-dependency

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-10
- Built MPICH libraries on EPEL (bz#1296387)
- Exclude OpenMPI on s390 arches
- Exclude MPICH on PPC arches

* Thu Jan 07 2016 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-9
- Built MPICH libraries (bz#1296387)
- Removed useless Requires packages

* Fri Nov 20 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-8
- Fixed links to OpenMPI-1.10.1 libraries on Fedora

* Fri Nov 20 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-7
- Fixed links to OpenMPI-1.6.4 libraries on EPEL7

* Wed Nov 18 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-6
- Fixed links to OpenMPI-1.10 libraries

* Mon Nov 16 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-5
- Set MPI libraries by using pkgconfig
- ExcludeArch s390x s390

* Fri Oct 30 2015 Antonio Trande <sagitter@fedoraproject.org> - 5.0.1-4
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
