import etcd3
import os
from oslo_utils import timeutils
import time

def get_etcd_client_v3(agent_host):
    ca_cert, cert, cert_key = _get_etcd_ssl(agent_host)
    return etcd3.client(host='localhost',
                        port=2379,
                        timeout=10,
                        cert_key=cert_key,
                        ca_cert=ca_cert,
                        cert_cert=cert)

def _get_etcd_ssl(agent_host):
    host_name = agent_host.rstrip('.domain.tld')

    # example: /etc/ssl/etcd/ssl/ca.pem
    ca_cert = os.path.join('/etc/ssl/etcd/ssl', 'ca.pem')

    # example: /etc/ssl/etcd/ssl/node-node-1.pem
    cert_name = 'node-%s.pem' % host_name
    cert = os.path.join('/etc/ssl/etcd/ssl', cert_name)

    # example: /etc/ssl/etcd/ssl/node-node-1-key.pem
    cert_key_name = 'node-%s-key.pem' % host_name
    cert_key = os.path.join('/etc/ssl/etcd/ssl', cert_key_name)

    return ca_cert, cert, cert_key
while True:
    with timeutils.StopWatch() as timer:
        client = get_etcd_client_v3('node-14.domain.tld')
        client.put('/openstack/easystack-hagent/testttt', 'test')
    print('Took %0.2f seconds to write to etcd.' % timer.elapsed())
    time.sleep(5)
