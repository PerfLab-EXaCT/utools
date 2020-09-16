-*-Mode: markdown;-*-
-----------------------------------------------------------------------------

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
  vtune_cmd="vtune -report hotspots -format csv -csv-delimiter comma -result-dir \"${dir}\""
  ${vtune_cmd} -report-output "${out1}"
  ${vtune_cmd} -report-output "${out2} -group-by=package"
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
