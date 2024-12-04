#!/bin/sh
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : v1.0.0
# update : 2024-12-04 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/sbin:/usr/local/bin
export LANG=en_US.UTF-8

date_day=$(date +%Y%m%d)
date_pre=$(date -d "1 days ago" +%m/%d/%Y)" 08:00:00"
work_dir="/usr/openv/scripts/nbuchk"
python3="/usr/local/python3/bin/python3"
log_file="${work_dir}/run.sh.log"
${is_sduo}
text_list="bpdbjobs client disk policy server tape"
csv_list="disk tape jobs policy sum"

master_list="nbu.forzw.com nbu83.forzw.com"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# define log head
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# use echo "$(get_msg_head) get xxx is: ${xxx}" >> $log_file

function get_msg_head()
{
millisecond=$(expr $(date +%N) / 1000000)
msg_head="$(date '+%Y-%m-%d %H:%M:%S').$(printf '%03d' ${millisecond}) -"
echo $msg_head
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# check process exist function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

check_file(){

    if [[ -f $1 ]]; then
        echo "$(get_msg_head) [OK] $1" >> $log_file
    else
        echo "$(get_msg_head) [NO] $1" >> $log_file
    fi
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# collect txt to csv function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

check_csv(){

    cd ${work_dir}

    for txt in ${text_list}
    do
        check_file tmp/${master}_${txt}_${date_day}.txt
    done

    ${python3} run.py --master ${master} --opr check_disk_used
    ${python3} run.py --master ${master} --opr check_tape_used
    ${python3} run.py --master ${master} --opr check_jobs_list
    ${python3} run.py --master ${master} --opr check_sum_used

    for csv in ${csv_list}
    do
        check_file csv/${master}_${csv}_${date_day}.csv
    done

}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# run clean 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function cln_files(){

${is_sduo} find ${work_dir}/tmp/ -type f -name "*.txt" -mtime +14 -exec rm -f {} \;
${is_sduo} find ${work_dir}/csv/ -type f -name "*.csv" -mtime +14 -exec rm -f {} \;
${is_sduo} find ${work_dir}/out/ -type f -name "*.xlsx" -mtime +14 -exec rm -f {} \;

}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# call function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# run csv export 
for master in ${master_list}
do
    check_csv
done

cln_files