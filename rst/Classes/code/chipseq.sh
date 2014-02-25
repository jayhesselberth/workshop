#! /usr/bin/env bash

#BSUB -J chipseq
#BSUB -o %J.out
#BSUB -e %J.err

data=/vol1/opt/data
fastqfile=$data/wgEncodeBroadHistoneHelas3H3k4me3StdRawDataRep1.fastq.gz
bwtindex=$data/hg19
chromsize=$data/hg19.chrom.sizes

expname="chipseq.hela.h3k4me3"
bamfile=$expname.bam

# run the alignment
bowtie2 -x $bwtindex -U $fastqfile \
    | samtools view -ShuF4 - \
    | samtools sort -o - aln.temp -m 8G \
    > $bamfile

# call peaks
macs2 callpeaks --treatment $bamfile --name $expname

# find motifs
fasta=/vol3/home/jhessel/ref/genomes/hg19/hg19.fa
peakfasta=$expname.peaks.fa
bedtools getfasta -fi $fasta -bed chipseq.bed -fo chipseq.peaks.fa
meme -nmotifs 100 -minw 6 -max2 20 $peakfasta

# make coverage plots in bedgraph and bigwig
bedgraph="$expname.bg"
bigwig="$expname.bw"
bedtools genomecov -ibam $bamfile -g $chromsize -bg > $bedgraph
bedGraphToBigWig $bedgraph $chromsize $bigwig

# this needs to be all on one line:
# track type=bigWig
# bigDataUrl="http://amc-sandbox.ucdenver.edu/~jhessel/