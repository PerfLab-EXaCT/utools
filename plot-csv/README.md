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
  grappolo-vtune-orkut-dram
  grappolo-vtune-orkut-pdax
  grappolo-vtune-orkut-kdax
  #
  grappolo-vtune-friendster-dram
  grappolo-vtune-friendster-pdax
  grappolo-vtune-friendster-kdax
  #
  grappolo-vtune-moliere2016-dram
  grappolo-vtune-moliere2016-pdax
  grappolo-vtune-moliere2016-kdax
  #
  grappolo-vtune-clueweb12-kdax
  grappolo-vtune-uk2014-kdax
)

# vtune -report summary

for path in "${myL[@]}" ; do
  path_new="${path//-vtune-/-}" ;
  out1="${path_new}-fn.csv"
  out2="${path_new}-pkg.csv"
  printf "${path} --> ${out1}\n"
  vtune_cmd='vtune -report hotspots -format csv -csv-delimiter comma -result-dir'
  ${vtune_cmd} "${path}" -report-output "${out1}"
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
