#!/usr/bin/env bash
#set -x
instance_id=$1
pool_name1="pool-9f7fd5c6e5614ba8b5016b0120670155"
ceph_config1="/etc/ceph/ceph1.conf"
pool_name2="pool-11b126eeb7ab40eb9f2afc8122b6a7ff"
ceph_config2="/etc/ceph/ceph2.conf"
rbd_device_prefix="volume"

function check_rbd_parent() {
    rbd_device=$1
	rbd_volumes_type=$(cinder show $rbd_device|grep volume_type|awk -F\| '{ print $3 }'|awk '{print $1}')
	case $rbd_volumes_type in
    YD_SG5_C01)
     rbd -p $pool_name1 info $rbd_device -c $config_config1| grep -q parent
     echo $?
     ;;
    YD_SG5_C02)
	 rbd -p $pool_name2 info $rbd_device -c $config_config2| grep -q parent
     echo $?
     ;;
    esac
    echo $?
}

function rbd_flatten() {
    rbd_device=$1
	rbd_volumes_type=$(cinder show $rbd_device|grep volume_type|awk -F\| '{ print $3 }'|awk '{print $1}')
	case $rbd_volumes_type in
    YD_SG5_C01)
	 rbd -p $pool_name1 flatten $1 -c $config_config1
	 ;;
    YD_SG5_C02)
	 rbd -p $pool_name2 flatten $1 -c $config_config2
	 ;;
    esac
}

echo "### Scan Instance information with id: $instance_id ###"
instance_device_info=$(nova show $instance_id | grep os-extended-volumes:volumes_attached)

#device_list=$(echo $instance_device_info | awk -F\| '{ print $3 }' | jq '.[].id' | sed s/\"//g)
device_list=$(echo $instance_device_info | awk -F\| '{ print $3 }' | grep -Po 'id[" :]+\K[^"]+')
# echo "Instance with id: $instance_id device list:\n$device_list"


for dev in $device_list
do
    echo "Check rbd_device parent with volume_id: $dev"
    if [ $(check_rbd_parent $rbd_device_prefix-$dev) == 0 ];then
        rbd_flatten $rbd_device_prefix-$dev
    else
        echo "No Parent require to flatten."
    fi
done

echo "Cleanup Finished."

#echo "Start cleaning source volume...."
#/root/xxz/scripts/delete_source_vol.sh $instance_id
