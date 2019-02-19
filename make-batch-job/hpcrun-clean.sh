#!/bin/bash

#****************************************************************************
# $HeadURL$
# $Id$
#
# Nathan Tallent
#****************************************************************************

#****************************************************************************
#
#****************************************************************************

toDir="0threads"

cmd=$0

#****************************************************************************

if [[ $1 =~ -(-)?h(elp)? ]] ; then
  cat  <<EOF
  usage: ${cmd} <hpctoolkit-measurements-dir>

  Retains only MPI rank data (moving thread data).
EOF
  exit
fi


arg_hpctkDir=$1

if [[ ! -d ${arg_hpctkDir} ]] ; then
    printf "bad <hpctoolkit-measurements-dir>: '${arg_hpctkDir}'\n"
    exit 1
fi

#****************************************************************************

src_path="${arg_hpctkDir}"
dst_path="${arg_hpctkDir}/${toDir}"

mkdir -p "${dst_path}"

mv "${src_path}"/*-??????-00[1-9]-*.{hpcrun,hpctrace}     "${dst_path}" \
    &> /dev/null
mv "${src_path}"/*-??????-0[1-9][0-9]-*.{hpcrun,hpctrace} "${dst_path}" \
    &> /dev/null

num_hpcrun=$(ls -1 "${src_path}"/*.hpcrun | wc -l)

printf "${arg_hpctkDir}: Retained ${num_hpcrun} MPI rank files\n"
