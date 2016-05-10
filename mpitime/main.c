// -*-Mode: C++;-*- // technically C99

//*BeginPNNLCopyright********************************************************
//
// $HeadURL$
// $Id$
//
//**********************************************************EndPNNLCopyright*

//***************************************************************************
// $HeadURL$
//
// Nathan Tallent
//***************************************************************************


#define DO_PAPI 0
#define DO_Junk 0
#define DO_Allreduce 0

//***************************************************************************
// system includes
//***************************************************************************

#define _GNU_SOURCE /*RTLD_NEXT*/

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#include <dlfcn.h>

//***************************************************************************
// 
//***************************************************************************

#include <mpi.h>

#if (DO_PAPI)
# include <papi.h>
#endif

//***************************************************************************
// local includes
//***************************************************************************

#define DECLARE_REAL_FN(type, realname) \
    static type * realname = NULL

#define GET_DLSYM(type, var, name)					\
  do {									\
    if (var == NULL) {							\
      dlerror();							\
      var = (type *) dlsym(RTLD_NEXT, #name);				\
      const char* err_str = dlerror();					\
      if (var == NULL) {						\
	fprintf(stderr, "dlsym(%s) failed: %s", #name , err_str);	\
      }									\
    }									\
  } while (0)


//***************************************************************************
// 
//***************************************************************************

#define MyName "mpitime"

static int myRank = 0;
static int numRanks = 0;
static double timeBeg_s = 0;
//static double timeBeg0_s = 0;

#if (DO_PAPI)
const int numPapiEvnts = 4;
int eventSet = PAPI_NULL;
#endif

static void
my_init();


//***************************************************************************
//
//***************************************************************************

#define PARMS_Init int* argc, char*** argv

typedef int mpi_init_fn(PARMS_Init);

DECLARE_REAL_FN(mpi_init_fn, real_mpi_init);

extern int
PMPI_Init(PARMS_Init)
{
  GET_DLSYM(mpi_init_fn, real_mpi_init, PMPI_Init);

  //timeBeg0_s = PMPI_Wtime(); // may be invalid before MPI_Init

  int ret_mpi = real_mpi_init(argc, argv);
  // INVARIANT: all ranks synchronized

  my_init();

  timeBeg_s = PMPI_Wtime();
  
  return ret_mpi;
}


#if 1 // tallent: apparently needed for GA-based applications...
extern int
MPI_Init(PARMS_Init)
{
  int ret_mpi = PMPI_Init(argc, argv);
  return ret_mpi;
}
#endif


static void
my_init()
{
  PMPI_Comm_rank(MPI_COMM_WORLD, &myRank);
  PMPI_Comm_size(MPI_COMM_WORLD, &numRanks);

#if 0
  fprintf(stderr, "rank: %d\n", myRank);
#endif


#if (DO_PAPI)
  int ret;

  ret = PAPI_library_init(PAPI_VER_CURRENT);
  if (ret != PAPI_VER_CURRENT && ret > 0) {
    fprintf(stderr, "PAPI_library_init %d: %s\n", ret, PAPI_strerror(ret));
  }

  if ( (ret = PAPI_create_eventset(&eventSet)) != PAPI_OK) {
    fprintf(stderr, "PAPI_create_eventset %d: %s\n", ret, PAPI_strerror(ret));
  }

  if ( (ret = PAPI_add_event(eventSet, PAPI_TOT_CYC)) != PAPI_OK) {
    fprintf(stderr, "PAPI_add_event1 %d: %s\n", ret, PAPI_strerror(ret));
  }
  if ( (ret = PAPI_add_event(eventSet, PAPI_FP_OPS)) != PAPI_OK) {
    fprintf(stderr, "PAPI_add_event2 %d: %s\n", ret, PAPI_strerror(ret));
  }

  int evcode;
  if ( (ret = PAPI_event_name_to_code("DISPATCH_STALL_FOR_FPU_FULL", &evcode)) != PAPI_OK) {
    fprintf(stderr, "PAPI_event_name_to_code1 %d: %s\n", ret, PAPI_strerror(ret));
  }
  if ( (ret = PAPI_add_event(eventSet, evcode)) != PAPI_OK) {
    fprintf(stderr, "PAPI_add_event3 %d: %s\n", ret, PAPI_strerror(ret));
  }

  if ( (ret = PAPI_event_name_to_code("L2_CACHE_MISS", &evcode)) != PAPI_OK) {
    fprintf(stderr, "PAPI_event_name_to_code2 %d: %s\n", ret, PAPI_strerror(ret));
  }
  if ( (ret = PAPI_add_event(eventSet, evcode)) != PAPI_OK) {
    fprintf(stderr, "PAPI_add_event4 %d: %s\n", ret, PAPI_strerror(ret));
  }
#endif
}

// extern int mpitimef_init()   __attribute__ ((weak, alias ("mpitime_init")));
// extern int mpitimef_init_()  __attribute__ ((weak, alias ("mpitime_init")));
// extern int mpitimef_init__() __attribute__ ((weak, alias ("mpitime_init")));


//***************************************************************************

typedef int mpi_fini_fn();

DECLARE_REAL_FN(mpi_fini_fn, real_mpi_fini);

extern int
PMPI_Finalize()
{
  GET_DLSYM(mpi_fini_fn, real_mpi_fini, PMPI_Finalize);

  double timeEnd0_s = PMPI_Wtime();

  // N.B.: 
  PMPI_Barrier(MPI_COMM_WORLD);
  // INVARIANT: all ranks synchronized

  double timeEnd_s = PMPI_Wtime();

  int ret_mpi = real_mpi_fini();

  //double timeEnd2_s = PMPI_Wtime(); // may be invalid after MPI_Finalize

  if (myRank == 0) {
    double time_s      = (timeEnd_s - timeBeg_s);

    double timeExcl_s  = (timeEnd0_s - timeBeg_s);
    //double timeIncl_s  = (timeEnd2_s - timeBeg0_s);

    //double time_init_s = (timeBeg_s - timeBeg0_s);
    //double time_fini_s = (timeEnd2_s - timeEnd0_s);

    fprintf(stderr, "*** " MyName " (s): %g (rank[0]: excl: %g) ***\n",
	    time_s, timeExcl_s /*, timeIncl_s, time_init_s, time_fini_s*/);
  }

  return ret_mpi;
}


#if 1 // tallent: apparently needed for GA-based applications...
extern int
MPI_Finalize()
{
  int ret_mpi = PMPI_Finalize();
  return ret_mpi;
}
#endif


//***************************************************************************
// Extra junk
//***************************************************************************

#if defined(DO_Junk) && DO_Junk

static double wtimeBeg_s = 0;

extern void
my_wtime_beg()
{
#if (DO_PAPI)
  int ret;
  if ( (ret = PAPI_start(eventSet)) != PAPI_OK) {
    fprintf(stderr, "PAPI_start %d: %s\n", ret, PAPI_strerror(ret));
  }
#else
  wtimeBeg_s = PMPI_Wtime();
#endif
}

extern int myf_wtime_beg()   __attribute__ ((weak, alias ("my_wtime_beg")));
extern int myf_wtime_beg_()  __attribute__ ((weak, alias ("my_wtime_beg")));
extern int myf_wtime_beg__() __attribute__ ((weak, alias ("my_wtime_beg")));


extern void
my_wtime_end(int name, int doSync, int info)
{
  static uint64_t numCalls = 0;
  
#if (DO_PAPI)
  long long values[numPapiEvnts];
  int ret;
  if ( (ret = PAPI_stop(eventSet, values)) != PAPI_OK) {
    fprintf(stderr, "PAPI_stop %d: %s\n", ret, PAPI_strerror(ret));
  }
#else
  double wtimeEnd_s = PMPI_Wtime();
#endif

  numCalls++;

  const int rank0 = 0;
  int rank1 = numCalls % numRanks;
  int rank2 = (numCalls + 7) % numRanks;

  PMPI_Barrier(MPI_COMM_WORLD);
  if (myRank == rank0 || myRank == rank1 || myRank == rank2) {
#if (DO_PAPI)
    fprintf(stderr, "*** " MyName "[%d]/time@%d {%d} (us): cyc %lu, fp %lu, stl %lu, l2m %lu ***\n",
	    myRank, name, info, values[0], values[1], values[2], values[3]);
#else
    double time_us = (wtimeEnd_s - wtimeBeg_s) * 1e6;
    fprintf(stderr, "*** " MyName "[%d]/time@%d {%d} (us): %g ***\n",
	    myRank, name, info, time_us);
#endif
  }

  if (doSync) {
    PMPI_Barrier(MPI_COMM_WORLD);
    // INVARIANT: resynchronize
  }
}


extern void
myf_wtime_end(int* name, int* doSync, int* info)
{
  my_wtime_end(*name, *doSync, *info);
}

extern int myf_wtime_end_()  __attribute__ ((weak, alias ("myf_wtime_end")));
extern int myf_wtime_end__() __attribute__ ((weak, alias ("myf_wtime_end")));

#endif


//***************************************************************************
// 
//***************************************************************************

#if defined(DO_Allreduce) && DO_Allreduce

#define PARMS_Allreduce \
  void *sendbuf, void *recvbuf, int count, \
  MPI_Datatype datatype, MPI_Op op, MPI_Comm comm

typedef int mpi_allreduce_fn(PARMS_Allreduce);

DECLARE_REAL_FN(mpi_allreduce_fn, real_mpi_allreduce);

int
PMPI_Allreduce(PARMS_Allreduce)
{
  GET_DLSYM(mpi_allreduce_fn, real_mpi_allreduce, PMPI_Allreduce);

#if 0
  PMPI_Barrier(comm); // should absorb load imbalance costs
#endif

  double timeBeg_s = PMPI_Wtime();

  int ret_mpi = real_mpi_allreduce(sendbuf, recvbuf, count, datatype, op, comm);
  // INVARIANT: synchronized

  double timeEnd_s = PMPI_Wtime();

  if (myRank == 0) {
    double time_us = (timeEnd_s - timeBeg_s) * 1e6;
    fprintf(stderr, "*** " MyName "/allreduce[0] (us): %g ***\n", time_us);
  }
  PMPI_Barrier(comm);
  // INVARIANT: resynchronize to avoid load imbalance

  return ret_mpi;
}

#endif
