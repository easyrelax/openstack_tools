#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from nova import config
from nova import context
from nova import exception
from nova import objects
from nova import rpc
from nova.virt import configdrive


def rm_config_drive(instance_uuid=None):
    ctxt = context.get_admin_context()
    if instance_uuid is not None:
        try:
            instance = objects.Instance.get_by_uuid(ctxt, instance_uuid)
            instances = [instance]
        except exception.InstanceNotFound as e:
            print(e.format_message())
            return
    else:
        instances = objects.InstanceList.get_all(ctxt)

    if instances:
        rm_manual = []
        for ins in instances:
            if ins.config_drive:
                print('Instance:%s remove config drive in db.' % ins.uuid)
                ins.config_drive = ''
                ins.save()
            elif configdrive.required_by(ins):
                rm_manual.append(ins.uuid)
        if rm_manual:
            print('Instances:%s with config drive by image or config '
                  'need rm manually.' % rm_manual)


def main():
    argv = sys.argv
    if len(argv) not in [1, 2]:
        print('Usage:python rm_config_drive [instance_uuid]')
        return
    print('------begin-----')
    config.parse_args([])
    objects.register_all()
    uuid = argv[1] if len(argv) == 2 else None
    rm_config_drive(uuid)
    rpc.cleanup()
    print('------end-----')


if __name__ == '__main__':
    main()
