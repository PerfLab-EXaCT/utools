-*-Mode: markdown;-*-
-----------------------------------------------------------------------------

mem: similar times, slightly more cost with kdax, which makes sense. 

---

Intel questions:
  - mlc random latency
  - near memory cache miss rate: l4_hit*
  - bw and latency histograms as textual reports?
  - new hypothesis

  - cycles vs pipeline stalls?
  
  MEMKIND_DAX_KMEM_INTERLEAVE

vtune: pmem dimms

EDP: 

Near memory cache = L4 miss rate as 


- Distributed memory (cost, power)

kdax supports numactl...

- Optane: Power, mem mode?

- New Optane:
  Barlow Pass (Ice Lake), new instructions
  Apache Pass (Cascade Lake)
  
- Intel GPUs
  

- GUPS results
  random access bandwidth, local/remote


- Grappolo: DRAM allocs were done by single thread. Use guarded, round-robin execution to ensure correct first-touch.


- Fig 4: reorder columns and labels?


- Ripples: tested two variants but had one more idea
  do we hit a bandwidth limitation?
  kdax2
  
  


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

myL=(
  soc-Slashdot0902.imm-dram.T64-vtune
  soc-Slashdot0902.imm-mem.T64-vtune
  soc-Slashdot0902.imm-kdax1.T64-vtune
  soc-Slashdot0902.imm-kdax2.T64-vtune
  soc-Slashdot0902.imm-kdax3.T64-vtune
  #
  soc-twitter-combined.imm-dram.T64-vtune
  soc-twitter-combined.imm-mem.T64-vtune
  soc-twitter-combined.imm-kdax1.T64-vtune
  soc-twitter-combined.imm-kdax2.T64-vtune
  soc-twitter-combined.imm-kdax3.T64-vtune
  #
  wiki-talk.imm-dram.T64-vtune
  wiki-talk.imm-mem.T64-vtune
  wiki-talk.imm-kdax1.T64-vtune
  wiki-talk.imm-kdax2.T64-vtune
  wiki-talk.imm-kdax3.T64-vtune
  #
  soc-pokec-relationships.imm-dram.T64-vtune
  soc-pokec-relationships.imm-mem.T64-vtune
  soc-pokec-relationships.imm-kdax1.T64-vtune
  soc-pokec-relationships.imm-kdax2.T64-vtune
  soc-pokec-relationships.imm-kdax3.T64-vtune
  #
  wiki-topcats.imm-mem.T64-vtune
  wiki-topcats.imm-kdax1.T64-vtune
  wiki-topcats.imm-kdax2.T64-vtune
  wiki-topcats.imm-kdax3.T64-vtune
)

# vtune -report summary
# vtune -report hotspots
# vtune -report hw-events

for path in "${myL[@]}" ; do
  report=hotspots # hw-events
  path=${path%/*} # strip trailing /
  path_new="${path//-vtune/}" ;
  out1="${path_new}-${report}-fn.csv"
  out2="${path_new}-${report}-pkg.csv"
  printf "${path} --> ${out1}\n"
  vtune_cmd="vtune -report ${report} -format csv -csv-delimiter comma -result-dir"
  ${vtune_cmd} "${path}" -report-output "${out1}" #-group-by=function
  ${vtune_cmd} "${path}" -report-output "${out2}" -group-by=package
done
```

```
dir=/files0/tallent/xxx-optane/grappolo
#dir=/files0/tallent/xxx-optane/ripples
for src in ${dir}/*.csv ; do
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
