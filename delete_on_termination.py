#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from oslo_utils import strutils
from nova import config
from nova import context
from nova import exception
from nova import objects
from nova import rpc


def delete_on_termination(instance_uuid, is_delete):
    ctxt = context.get_admin_context()
    if instance_uuid is not None:
        try:
            instances = [objects.Instance.get_by_uuid(ctxt, instance_uuid)]
        except exception.InstanceNotFound as e:
            print(e.format_message())
            return
    else:
        instances = objects.InstanceList.get_all(ctxt)
    bdms = objects.BlockDeviceMappingList.get_by_instance_uuids(
        ctxt, [i.uuid for i in instances])
    if instance_uuid is not None:
        for bdm in bdms:
            if bdm.delete_on_termination != is_delete:
                print('change instance:%s with bdm:%s '
                      'delete_on_termination %s to %s' %
                      (bdm.instance_uuid, bdm.volume_id,
                       bdm.delete_on_termination, is_delete))
                bdm.delete_on_termination = is_delete
                bdm.save()
    else:
        delete_on_termination_bdms = [bdm for bdm in bdms if bdm.delete_on_termination]
        if delete_on_termination_bdms:
            for bdm in delete_on_termination_bdms:
                print('change instance:%s with bdm:%s '
                      'delete_on_termination %s to False' %
                      (bdm.instance_uuid, bdm.volume_id,
                       bdm.delete_on_termination))
                bdm.delete_on_termination = False
                bdm.save()

def main():
    argv = sys.argv
    if len(argv) not in [1, 3]:
        print('Usage:python delete_on_termination.py [instance_uuid] [True/False]')
        return
    print('------begin-----')
    config.parse_args([])
    objects.register_all()
    instance_uuid = None if len(argv) == 1 else argv[1]
    delete = False if len(argv) == 1 else argv[2]
    delete = strutils.bool_from_string(delete)
    delete_on_termination(instance_uuid, delete)
    rpc.cleanup()
    print('------end-----')


if __name__ == '__main__':
    main()
