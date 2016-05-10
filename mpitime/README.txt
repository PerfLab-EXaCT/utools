Notes on overriding MPI routines:

  - Compiled object code calls MPI_*/mpi_*.

  - Typically, MPI libraries are implemented in the following manner:

    - The MPI_*/mpi_* routines are weak symbols that point to their
      corresponding (strong) PMPI_*/pmpi_* symbols.  (See 14.2.6 of MPI
      3.0 standard.)
   
    - A Fortran routine mpi_x (pmpi_x) uses its C variant
      (MPI_x/PMPI_x) as a common implementation (along with some
      argument packing/unpacking).

    - If MPI_x is not supplied by the user, the fully linked code
      will call PMPI_x.

  - For dynamically linked binaries:

    - Typically, it is possible to override only strong symbols
      (via LD_PRELOAD).

    - Thus, it is sufficient to override only C PMPI_* routines.

  - For statically linked binaries
    - GNU ld --wrap can wrap weak or strong symbols 
    
    - Thus, it is sufficient to wrap only C PMPI_* routines.  (If
      we wrap MPI_*/mpi_* routines, then it is necessary to handle
      all C and Fortran entry points.)

*** On ARGOS, it is necessary to override MPI_Init (not PMPI_Init) ***
    This relates somehow to GA...
