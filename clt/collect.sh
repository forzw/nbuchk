#!/bin/sh
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : v1.0.0
# update : 2024-11-30 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/sbin:/usr/local/bin
export LANG=en_US.UTF-8

date_day=$(date +%Y%m%d)
date_pre=$(date -d "1 days ago" +%m/%d/%Y)" 08:00:00"
work_dir="/usr/openv/scripts/nbuchk"
ssh_host="red.forzw.com"
ssh_user="root"
ssh_pass="password"
log_file="${work_dir}/logs/collect.log"

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
# check master connect
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function pre_collect(){

if [[ ! -f "/usr/openv/netbackup/bp.conf" ]]; then
    echo "$(get_msg_head) Not found NetBackup, exit scripts. " >> $log_file
    exit 1
fi

master_name=$(head -1 /usr/openv/netbackup/bp.conf |awk '{print $3}')

if [[ ${master_name} == "" ]]; then
    echo "$(get_msg_head) Get master failed, exit scripts. " >> $log_file
    exit 1
fi

jobs_file="${work_dir}/tmp/${master_name}_bpdbjobs_${date_day}.txt"
disk_file="${work_dir}/tmp/${master_name}_disk_${date_day}.txt"
tape_file="${work_dir}/tmp/${master_name}_tape_${date_day}.txt"
policy_file="${work_dir}/tmp/${master_name}_policy_${date_day}.txt"
server_file="${work_dir}/tmp/${master_name}_server_${date_day}.txt"
client_file="${work_dir}/tmp/${master_name}_client_${date_day}.txt"


if [[ ! -d ${work_dir}/tmp ]];then
    echo "$(get_msg_head) create tmp dir ${work_dir}/tmp/" >> $log_file
    mkdir -p ${work_dir}/tmp/
fi


}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# run collect
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function run_collect(){

# 1,get jobs

/usr/openv/netbackup/bin/admincmd/bpdbjobs -t ${date_pre} -json > ${jobs_file}

if [[ $? == 0 ]]; then
    echo "$(get_msg_head) Successfull collect NetBackup Jobs. " >> $log_file
else
    echo "$(get_msg_head) Failed collect NetBackup Jobs with $?. " >> $log_file
fi


# 2,get disk

/usr/openv/netbackup/bin/admincmd/nbdevquery -listdv -stype PureDisk -L > ${disk_file}

if [[ $? == 0 ]]; then
    echo "$(get_msg_head) Successfull collect NetBackup Disk. " >> $log_file
else
    echo "$(get_msg_head) Failed collect NetBackup Disk with $?. " >> $log_file
fi


# 3,get tape

/usr/openv/netbackup/bin/goodies/available_media > ${tape_file}

if [[ $? == 0 ]]; then
    echo "$(get_msg_head) Successfull collect NetBackup Tape. " >> $log_file
else
    echo "$(get_msg_head) Failed collect NetBackup Tape with $?. " >> $log_file
fi


# 4,get active policy list

/usr/openv/netbackup/bin/admincmd/bppllist -L -allpolicies|awk '/Policy Name:/{a=$3}/Active:            yes/{print a}' > ${policy_file}

if [[ $? == 0 ]]; then
    echo "$(get_msg_head) Successfull collect NetBackup Policy. " >> $log_file
else
    echo "$(get_msg_head) Failed collect NetBackup Policy with $?. " >> $log_file
fi

# 5,get media server list

/usr/openv/netbackup/bin/admincmd/nbemmcmd -listhosts |grep media|awk '{print $2}' > ${server_file}

if [[ $? == 0 ]]; then
    echo "$(get_msg_head) Successfull collect NetBackup Server. " >> $log_file
else
    echo "$(get_msg_head) Failed collect NetBackup Server with $?. " >> $log_file
fi

# 6,get client list

/usr/openv/netbackup/bin/admincmd/bpplclients |tail -n +3|awk '{print $3}' > ${client_file}


if [[ $? == 0 ]]; then
    echo "$(get_msg_head) Successfull collect NetBackup Clients. " >> $log_file
else
    echo "$(get_msg_head) Failed collect NetBackup Clients with $?. " >> $log_file
fi


}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# run push file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function scp_pass_collect(){

chmod 775 ${work_dir}/tmp/*_${date_day}.txt

for file in `ls -a ${work_dir}/tmp/*_${date_day}.txt`
do
    expect ${work_dir}/nbuchk_login.exp ${ssh_host} ${ssh_user} ${ssh_pass} ${file} ${work_dir}/tmp/
done 

if [[ $? == 0 ]]; then
    echo "$(get_msg_head) Successfull scp files to ${ssh_host}:${work_dir}/tmp/. " >> $log_file
else
    echo "$(get_msg_head) Failed scp files to ${ssh_host}:${work_dir}/tmp/ with $?. " >> $log_file
fi

}

function scp_collect(){

chmod 775 ${work_dir}/tmp/*_${date_day}.txt

scp ${work_dir}/tmp/*_${date_day}.txt ${ssh_user}@{ssh_host}:${work_dir}/tmp/ 

if [[ $? == 0 ]]; then
    echo "$(get_msg_head) Successfull scp files to ${ssh_host}:${work_dir}/tmp/. " >> $log_file
else
    echo "$(get_msg_head) Failed scp files to ${ssh_host}:${work_dir}/tmp/ with $?. " >> $log_file
fi

}



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# run clean 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function cln_collect(){

find ${work_dir}/tmp/ -type f -name "${master_name}_*.txt" -mtime +7 -exec rm -f {} \;

}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# call funtion 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pre_collect
run_collect
scp_collect
cln_collect
