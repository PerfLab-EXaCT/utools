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

#****************************************************************************

scriptPath="${BASH_SOURCE[0]}" # works when script is sourced (unlike $0)
scriptCmd=${scriptPath##*/} # cf. $(basename ...)


if [[ $1 =~ -(-)?h(elp)? ]] ; then
  cat  <<EOF
  usage: ${scriptCmd} <hpctoolkit-measurements-dir>

  Retains only MPI rank data (moving thread data to '${toDir}').
EOF
  exit
fi


#-----------------------------------------------------------
#
#-----------------------------------------------------------

arg_hpctkDir="$1"

if [[ ! -d ${arg_hpctkDir} ]] ; then
    printf "bad <hpctoolkit-measurements-dir>: '${arg_hpctkDir}'\n"
    exit 1
fi

#****************************************************************************

src_path="${arg_hpctkDir}"
dst_path="${arg_hpctkDir}/${toDir}"

mkdir -p "${dst_path}"

mv -n "${src_path}"/*-??????-00[1-9]-*.{hpcrun,hpctrace}     "${dst_path}" \
    &> /dev/null
mv -n "${src_path}"/*-??????-0[1-9][0-9]-*.{hpcrun,hpctrace} "${dst_path}" \
    &> /dev/null


#-----------------------------------------------------------
#
#-----------------------------------------------------------

num_hpcrun=$(ls -1 "${src_path}"/*.hpcrun | wc -l)

printf "${arg_hpctkDir}: Retained ${num_hpcrun} MPI rank files\n"
