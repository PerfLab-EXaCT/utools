-*-Mode: markdown;-*-
-----------------------------------------------------------------------------

Hardware Event Count:CYCLE_ACTIVITY.STALLS_L1D_MISS

total memory subsystem: CYCLE_ACTIVITY.STALLS_MEM_ANY + EXE_ACTIVITY.BOUND_ON_STORES

L1-bound: max(CYCLE_ACTIVITY.STALLS_MEM_ANY - CYCLE_ACTIVITY.STALLS_L1D_MISS, 0)
L2-bound: (CYCLE_ACTIVITY.STALLS_L1D_MISS - CYCLE_ACTIVITY.STALLS_L2_MISS)
L3-bound: (CYCLE_ACTIVITY.STALLS_L2_MISS - CYCLE_ACTIVITY.STALLS_L3_MISS)
mem-bound: CYCLE_ACTIVITY.STALLS_L3_MISS
store-bound: EXE_ACTIVITY.BOUND_ON_STORES




- GUPS results
  random access bandwidth, local/remote

- Grappolo: DRAM allocs were done by single thread. Use guarded, round-robin execution to ensure correct first-touch.

- Fig 4: reorder columns and labels?

- Ripples: tested two variants but had one more idea
  do we hit a bandwidth limitation?
  kdax2
  

- One more month. Any more experiments?

  libpmem, streaming
  

memkind NUMA: is it inflexible? ignores numactl?



Using
=============================================================================

0. Obtain VTune report (as .csv)

```
vtune -report hotspots -format csv -csv-delimiter comma \
  -result-dir <dir> \
  -report-output <out-file>

  -group-by=package \
```


1. View raw data:

```sh
./VtuneCSV.py <csv-file>
```

2. Plot

```sh
./plot-csv.py # ./data
```

Tests
=============================================================================

```sh
./plot-t0.py # ./data0/advanced-hotspots.csv
./plot-t1.py # ./data0/progression/*.csv
```


Example
=============================================================================

0. Obtain VTune report (as .csv)

```
myL=(
  grappolo-vtune-friendster-t192-dram
  grappolo-vtune-friendster-t192-mem
  grappolo-vtune-friendster-t192-kdax
  grappolo-vtune-friendster-t192-pdax
  #
  grappolo-vtune-moliere2016-t192-dram
  grappolo-vtune-moliere2016-t192-mem
  grappolo-vtune-moliere2016-t192-kdax
  grappolo-vtune-moliere2016-t192-pdax
  #
  grappolo-vtune-uk2014-t192-mem
  grappolo-vtune-uk2014-t192-kdax
  #
  grappolo-vtune-clueweb12-t192-mem
  grappolo-vtune-clueweb12-t192-kdax
)

# vtune -report summary
# vtune -report hotspots
# vtune -report hw-events

for path in "${myL[@]}" ; do
  report='hotspots'
  path=${path%/*} # strip trailing /
  path_new="${path//-vtune-/-}" ;
  out1="${path_new}-${report}-fn.csv"
  out2="${path_new}-${report}-pkg.csv"
  printf "${path} --> ${out1}\n"
  vtune_cmd='vtune -report ${report} -format csv -csv-delimiter comma -result-dir'
  ${vtune_cmd} "${path}" -report-output "${out1}" #-group-by=function
  ${vtune_cmd} "${path}" -report-output "${out2}" -group-by=package
done
```

```
for src in /files0/tallent/xxx-optane/grappolo/*.csv ; do
  csv=$(basename ${src})
  if ! diff ${src} ${csv} >& /dev/null ; then
    echo ${csv}
    cp ${src} ${csv}
  fi
done
```


1. Plot

```sh
./plot-csv.py # ./data
```


Acks:
=============================================================================

Initial based on https://github.com/pvelesko/vtune-plot

./plot-csv.py based on 'plot_progression.py'
