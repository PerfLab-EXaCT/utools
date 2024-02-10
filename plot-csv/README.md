<!-- -*-Mode: markdown;-*- -->
<!-- $Id$ -->

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

1. Plot

```sh
./plot-csv.py # ./data
```


Acks:
=============================================================================

Initial based on https://github.com/pvelesko/vtune-plot

./plot-csv.py based on 'plot_progression.py'
