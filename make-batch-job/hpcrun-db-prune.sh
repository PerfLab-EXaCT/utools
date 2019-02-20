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

toDir="0extra"

do_dryrun=0

#****************************************************************************

scriptPath="${BASH_SOURCE[0]}" # works when script is sourced (unlike $0)
scriptCmd=${scriptPath##*/} # cf. $(basename ...)

if [[ $1 =~ -(-)?h(elp)? ]] ; then
    cat  <<EOF
  usage: ${scriptCmd} <hpctoolkit-measurements-dir> <upper-bound> <stride>

  Prune MPI rank data in a strided fashion. Moves pruned data to '${toDir}'.
EOF
    exit
fi


if [[ $1 =~ -(-)dry(run)? ]] ; then
    do_dryrun=1
    shift
fi


#-----------------------------------------------------------
#
#-----------------------------------------------------------

arg_hpctkDir="$1"

if [[ ! -d ${arg_hpctkDir} ]] ; then
    printf "bad <hpctoolkit-measurements-dir>: '${arg_hpctkDir}'\n"
    exit 1
fi

#-----------------------------------------------------------
#
#-----------------------------------------------------------

ub_int="$2"

stride_real="$3"

lb_int=$(printf "%.f\n" $(echo "${stride_real} - 1" | bc))


if [[ -z ${ub_int} || -z ${stride_real} ]]; then
    printf "bad specification: upper: '${ub_int}'; stride: '${stride_real}'\n"
    exit 1
fi

#****************************************************************************

src_path="${arg_hpctkDir}"
dst_path="${arg_hpctkDir}/${toDir}"

mkdir -p "${dst_path}"

printf "${arg_hpctkDir}: Pruning data from ranks ${lb_int}-${ub_int}:${stride_real}\n"

i_real="${lb_int}"
for (( i_int = lb_int; i <= ub_int; )) ; do
    pid=$(printf "%06d" ${i_int})
    fnm_glob="*-${pid}-000-*.{hpcrun,hpctrace,log}"

    fileL=$(eval ls -1 "${src_path}"/${fnm_glob} 2> /dev/null)
    #fileL=$(eval compgen -G -- "${src_path}"/${fnm_glob} 2> /dev/null)
    #printf "list: ${fileL}\n"
      
    for fnm in ${fileL} ; do
	fnm_base=${fnm##*/} # cf. $(basename ...)
	printf "move: ${fnm_base} -> ${toDir}\n"
	if (( ! ${do_dryrun} )) ; then
	    \mv -n "${fnm}" "${dst_path}"
	fi
    done
   
    if [[ -z ${fileL} ]] ; then
	printf "skip: ${fnm_glob}\n"
    fi

    # if mv -n "${src_path}"/${fnm_glob} "${dst_path}" 2> /dev/null ; then
    #     printf "move: ${fnm_glob} -> ${dst_path}\n"
    # else
    #     printf "skip: ${fnm_glob}\n"
    # fi

    i_real=$(echo "${i_real} + ${stride_real}" | bc) # scale=0;
    i_int=$(printf "%.f\n" ${i_real})
done


#-----------------------------------------------------------
#
#-----------------------------------------------------------

num_hpcrun=$(ls -1 "${src_path}"/*.hpcrun | wc -l)

printf "${arg_hpctkDir}: Retained ${num_hpcrun} MPI rank files\n"
