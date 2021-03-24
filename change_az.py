#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from nova import availability_zones
from nova import config
from nova import context
from nova import exception
from nova import objects
from nova import rpc


def change_az(instance_uuid, az=None):
    ctxt = context.get_admin_context()
    print("------Deal with instance:%s--------" % instance_uuid)

    try:
        instance = objects.Instance.get_by_uuid(ctxt, instance_uuid)
    except exception.InstanceNotFound as e:
        print(e.format_message())
        return
    if az is None:
        az = availability_zones.get_host_availability_zone(ctxt, instance.host)
        print('Instance host:%s in AZ:%s, so change az to it.' % (
            instance.host, az))
    print('Instance %s origin az is:%s' % (instance_uuid,
                                           instance.availability_zone))
    if instance.availability_zone != az:
        print('Change instance %s AZ to:%s' % (instance_uuid, az))
        instance.availability_zone = az
        instance.save()
    else:
        print('Instance AZ is same with %s, no change.' % az)
    try:
        req = objects.RequestSpec.get_by_instance_uuid(ctxt, instance_uuid)
    except exception.RequestSpecNotFound as e:
        print(e.format_message())
        return
    print('Instance %s origin scheduler AZ is:%s' % (instance_uuid,
                                                     req.availability_zone))
    if req.availability_zone != az:
        print('Change instance %s scheduler AZ to:%s' % (instance_uuid, az))
        req.availability_zone = az
        req.save()
    else:
        print('Instance scheduler AZ is same with %s, no change.' % az)


def main():
    argv = sys.argv
    if len(argv) not in [2, 3]:
        print('Usage:python change_az <instance_uuid> [az]')
        return
    print('------begin-----')
    config.parse_args([])
    objects.register_all()
    az = argv[2] if len(argv) == 3 else None
    change_az(argv[1], az)
    rpc.cleanup()
    print('------end-----')


if __name__ == '__main__':
    main()
