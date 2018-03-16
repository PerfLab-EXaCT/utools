#!/bin/bash

#****************************************************************************
#
#****************************************************************************

i_ub="$1"
i_stride="$2"

((i_lb = i_stride - 1))

todir="./xtra"

#-----------------------------------------------------------
#
#-----------------------------------------------------------

if test -z "${i_ub}" -o -z "${i_stride}"; then
  cat  <<EOF
  usage: $0 <upper-bound> <stride>

  Execute from within <hpctoolkit-measurements-dir>
EOF

  exit 1
fi

mkdir -p "${todir}"

if test ! -d "${todir}" ; then
  echo "target directory '${todir}' does not exist"
  exit 1
fi

echo "Moving hpcrun data from ranks ${i_lb}--${i_ub}:${i_stride} to '${todir}'."

#-----------------------------------------------------------
#
#-----------------------------------------------------------

for (( i = i_lb; i <= i_ub; i = i + i_stride )) ; do
   path="."
   pid=`printf "%06d" ${i}`
   fnm_glob="${path}/*-${pid}-000-*.{hpcrun,log}"

   unset did_find
   for fnm in `eval ls -1 ${fnm_glob} 2> /dev/null` ; do
     did_find="yes"
     echo "moving: ${fnm} -> ${todir}/"
     mv -f "${fnm}" "${todir}"/
   done

   if test -z "${did_find}" ; then
     echo "skipping: ${fnm_glob}"
   fi
done
