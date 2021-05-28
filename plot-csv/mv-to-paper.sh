dst=/Users/tallent/1research/papers/optane-graphs/optane-graphs.overleaf-git/fig

myL=(
    chart-teaser1.pdf
    chart-teaser2.pdf

    chart-grappolo-scaling.pdf
    chart-grappolo-fn1.pdf
    chart-grappolo-fn2.pdf
    chart-grappolo-fn3.pdf
    chart-grappolo-fn4.pdf
    
    chart-ripples-scaling.pdf
    chart-ripples-fn1.pdf
    chart-ripples-fn2.pdf
    chart-ripples-fn3.pdf
    chart-ripples-fn4.pdf
    chart-ripples-fn5.pdf

    streambench-bw.pdf
    streambench-lat.pdf
)

for src in "${myL[@]}" ; do
    if [[ $src =~ grap ]] ; then
        dst2="/grappolo/"
    elif [[ $src =~ ripp ]] ; then
        dst2="/imm/"
    else
        dst2="/"
    fi
    
    if [[ -r ${src} ]]; then
        pdfcrop ${src} ${src}
        mv ${src} ${dst}${dst2}
    fi
done
