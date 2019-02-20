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

i_ub="$2"
i_stride="$3"

((i_lb = i_stride - 1))

if [[ -z ${i_ub} || -z ${i_stride} ]]; then
    printf "bad stride specification: upper: '${i_ub}'; stride: '${i_stride}'\n"
    exit 1
fi

#****************************************************************************

src_path="${arg_hpctkDir}"
dst_path="${arg_hpctkDir}/${toDir}"

mkdir -p "${dst_path}"

printf "${arg_hpctkDir}: Pruning data from ranks ${i_lb}-${i_ub}:${i_stride}\n"

for (( i = i_lb; i <= i_ub; i = i + i_stride )) ; do
   pid=$(printf "%06d" ${i})
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
done
