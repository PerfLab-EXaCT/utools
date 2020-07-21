-*-Mode: markdown;-*-
-----------------------------------------------------------------------------


Using
=============================================================================

```
vtune -report hotspots -format csv -csv-delimiter comma \
  -result-dir <dir> \
  -report-output <out-file>

  -group-by=package \
```


```sh
./VtuneCSV.py ./data0/progression/*.csv
./VtuneCSV.py ./data0/advanced-hotspots.csv

./plot-csv.py ./data0/progression/*.csv

./plot_pie.py ./data0/advanced-hotspots.csv
```

-----------------------------------------------------------------------------

```
myL=(
  grappolo-vtune-profile-friendster-optane-appdirect-dram
  grappolo-vtune-profile-friendster-optane-appdirect-pmem
  grappolo-vtune-profile-moliere2016-optane-appdirect-dram
  grappolo-vtune-profile-moliere2016-optane-appdirect-pmem
  grappolo-vtune-profile-orkut-optane-appdirect-dram
  grappolo-vtune-profile-orkut-optane-appdirect-pmem
)

for dir in "${myL[@]}" ; do
  out1="${dir}-fn.csv"
  out2="${dir}-pkg.csv"
  printf "${dir} --> ${out1}\n"
  vtune -report hotspots -format csv -csv-delimiter comma \
    -result-dir "${dir}" \
    -report-output "${out1}"
  vtune -report hotspots -format csv -csv-delimiter comma \
    -group-by=package \
    -result-dir "${dir}" \
    -report-output "${out2}"
done
```


Function / Memory Object / Allocation Stack	CPU Time	L1 Bound	L2 Bound	L3 Bound	DRAM Bound	Store Bound	Persistent Memory Bound	Loads	Stores	LLC Miss Count	Average Latency (cycles)	Start Address
_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)1, (bool)0, (bool)1>	54.4%	9.4%	0.0%	0.0%	0.0%	0.0%	0.0%	1,570,112,101,950	143,854,315,500	0	7	0x62210
buildLocalMapCounter	20.8%	6.7%	31.7%	14.6%	13.7%	0.0%	0.0%	465,870,975,710	47,573,427,160	217,015,190	16	0x43d580
sumVertexDegree$omp$parallel_for@74	5.5%	0.0%	0.0%	3.7%	75.3%	0.0%	0.0%	168,005,040	7,000,210	0	0	0x43cfcc
[vmlinux]	4.5%	13.9%	0.3%	1.4%	1.9%	6.7%	0.0%	99,423,982,630	49,617,488,480	21,001,470	10	0
_INTERNAL_25_______src_kmp_barrier_cpp_ddfed41b::__kmp_wait_template<kmp_flag_64, (int)0, (bool)0, (bool)1>	1.8%	7.1%	0.0%	0.0%	0.0%	0.0%	0.0%	50,058,501,710	4,725,141,750	0	7	0x62cf8
std::_Rb_tree_insert_and_rebalance	1.5%	22.6%	1.5%	0.6%	0.7%	0.0%	0.0%	51,759,552,740	27,447,823,410	0	7	0xab0d0
_int_free	1.5%	14.6%	1.2%	0.3%	0.3%	0.9%	0.0%	76,127,283,750	33,622,008,630	0	9	0x91e90
max	1.4%	4.1%	6.3%	11.0%	25.3%	0.0%	0.0%	31,633,948,990	1,092,032,760	7,000,490	15	0x43e090
__GI___libc_malloc	1.1%	14.9%	3.1%	0.1%	1.2%	0.0%	0.0%	39,243,177,260	8,995,269,850	0	8	0x95b90
_int_malloc	1.0%	28.1%	4.7%	1.3%	2.1%	0.1%	0.0%	23,632,708,960	15,596,467,880	0	20	0x93660



Acks:
=============================================================================

Initial based on https://github.com/pvelesko/vtune-plot

./plot-csv.py based on 'plot_progression.py'
