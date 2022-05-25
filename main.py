#!/usr/bin/python3

"""
SpeedTest
"""

import os
import json
import sqlite3

# persistence
_db = None


def db(forceinit=False):
    global _db

    # Initialize database connection
    if _db is None:
        _db = sqlite3.connect('/home/pi/speedtest/speedtest.db')
        forceinit = True

    # Initialize database table with a transaction
    if forceinit is True:
        _db.cursor().execute("""CREATE TABLE IF NOT EXISTS log (
            type text,
            timestamp text,
            ping_jitter text,
            ping_latency text,
            download_bandwidth text,
            download_bytes text,
            download_elapsed text,
            upload_bandwidth text,
            upload_bytes text,
            upload_elapsed text,
            packetLoss text,
            isp text,
            interface_internalIp text,
            interface_name text,
            interface_macAddr text,
            interface_isVpn text,
            interface_externalIp text,
            server_id text,
            server_host text,
            server_port text,
            server_name text,
            server_location text,
            server_country text,
            server_ip text,
            result_id text,
            result_url text,
            result_persisted text
            )
        """)
        # commit transaction
        _db.commit()

    # return
    return _db


def get_sample():
    db().cursor().execute("""SELECT
        type,
        timestamp,
        ping_jitter,
        ping_latency,
        download_bandwidth,
        download_bytes,
        download_elapsed,
        upload_bandwidth,
        upload_bytes,
        upload_elapsed,
        packetLoss,
        isp,
        interface_internalIp,
        interface_name,
        interface_macAddr,
        interface_isVpn,
        interface_externalIp,
        server_id,
        server_host,
        server_port,
        server_name,
        server_location,
        server_country,
        server_ip,
        result_id,
        result_url,
        result_persisted
            FROM log where timestamp = max(timestamp)
            LIMIT 0,1
    """)
    return db.cursor().fetchone


def record_sample():
    # https://www.speedtest.net/apps/cli
    # armhf (ie pi):
    # https://install.speedtest.net/app/cli/ookla-speedtest-1.1.1-linux-armhf.tgz

    # create a pipe to a forked shell and run a commandin it
    stream = os.popen('/home/pi/speedtest/speedtest -f json --output-header')

    # read the stream (stdout of the command we ran)
    output = stream.read()

    # import the output to a python dictionary
    external_data = json.loads(output)

    # convert the output to local format
    local_data = {
        'type': external_data['type'],
        'timestamp': external_data['timestamp'],
        'ping_jitter': external_data['ping']['jitter'],
        'ping_latency': external_data['ping']['latency'],
        'download_bandwidth': external_data['download']['bandwidth'],
        'download_bytes': external_data['download']['bytes'],
        'download_elapsed': external_data['download']['elapsed'],
        'upload_bandwidth': external_data['upload']['bandwidth'],
        'upload_bytes': external_data['upload']['bytes'],
        'upload_elapsed': external_data['upload']['elapsed'],
        'packetLoss': external_data['packetLoss'],
        'isp': external_data['isp'],
        'interface_internalIp': external_data['interface']['internalIp'],
        'interface_name': external_data['interface']['name'],
        'interface_macAddr': external_data['interface']['macAddr'],
        'interface_isVpn': external_data['interface']['isVpn'],
        'interface_externalIp': external_data['interface']['externalIp'],
        'server_id': external_data['server']['id'],
        'server_host': external_data['server']['host'],
        'server_port': external_data['server']['port'],
        'server_name': external_data['server']['name'],
        'server_location': external_data['server']['location'],
        'server_country': external_data['server']['country'],
        'server_ip': external_data['server']['ip'],
        'result_id': external_data['result']['id'],
        'result_url': external_data['result']['url'],
        'result_persisted': external_data['result']['persisted']
    }

    # insert record
    db().cursor().execute("""insert into log (
        type,
        timestamp,
        ping_jitter,
        ping_latency,
        download_bandwidth,
        download_bytes,
        download_elapsed,
        upload_bandwidth,
        upload_bytes,
        upload_elapsed,
        packetLoss,
        isp,
        interface_internalIp,
        interface_name,
        interface_macAddr,
        interface_isVpn,
        interface_externalIp,
        server_id,
        server_host,
        server_port,
        server_name,
        server_location,
        server_country,
        server_ip,
        result_id,
        result_url,
        result_persisted
    ) values (
        :type,
        :timestamp,
        :ping_jitter,
        :ping_latency,
        :download_bandwidth,
        :download_bytes,
        :download_elapsed,
        :upload_bandwidth,
        :upload_bytes,
        :upload_elapsed,
        :packetLoss,
        :isp,
        :interface_internalIp,
        :interface_name,
        :interface_macAddr,
        :interface_isVpn,
        :interface_externalIp,
        :server_id,
        :server_host,
        :server_port,
        :server_name,
        :server_location,
        :server_country,
        :server_ip,
        :result_id,
        :result_url,
        :result_persisted)
    """, local_data)
    db().commit()

    return True


if __name__ == '__main__':
    record_sample()
    print(getsample())
