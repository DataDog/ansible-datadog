#!/usr/bin/env/python

import re
from checks import AgentCheck

class mdCheck(AgentCheck):
    def check(self, instance):
        if 'device' not in instance:
            self.log.info("Skipping instance, no device specified.")
            return

        # Load values from the instance config
        device = instance['device']

        mdList = self.parseMdstat()

        try:
             mdList[device]
        except:
            self.log.error("Device not found: %s" % device)
            return

        array_active            = len(mdList[device]['active'])
        array_spare             = len(mdList[device]['spare'])
        array_failed            = len(mdList[device]['failed'])
        array_total             = mdList[device]['total']
        array_up                = mdList[device]['up']
        array_recovery_complete = float(mdList[device]['recovery_complete'])/100
        array_recovery_speed    = float(mdList[device]['recovery_speed'])*1024

        self.gauge('md_device.disk.total', array_total, device_name=device)
        self.gauge('md_device.disk.active', array_active, device_name=device)
        self.gauge('md_device.disk.spare', array_spare, device_name=device)
        self.gauge('md_device.disk.failed', array_failed, device_name=device)
        self.gauge('md_device.disk.up', array_up, device_name=device)
        self.gauge('md_device.recovery.complete', array_recovery_complete, device_name=device)
        self.gauge('md_device.recovery.speed_bytes', array_recovery_speed, device_name=device)

    def parseMdstat(self):
        try:
            f_mdstat = open('/proc/mdstat', 'r')
        except:
            self.log.error("Can't open mdstat.")
            return

        mds_list = {}

        while True:
            line = f_mdstat.readline()
            if not line: break
            if re.match("md", line):
                meta = line.split(' ')
                device_name = meta[0]
                mds_list[device_name] = {}
                mds_list[device_name]['active'] = []
                mds_list[device_name]['failed'] = []
                mds_list[device_name]['spare']  = []
                for item in meta:
                    if re.match('raid',item):
                        raid_level=item
                        continue
                    if re.match('(\w+)\[\d+\](\(.\))*',item):
                        dev = re.search('(\w+)\[\d+\](\(F\))',item)
                        if dev:
                            mds_list[device_name]['failed'].append(dev.group(1))
                            continue
                        dev = re.search('(\w+)\[\d+\](\(S\))',item)
                        if dev:
                            mds_list[device_name]['spare'].append(dev.group(1))
                            continue
                        dev = re.search('(\w+)\[\d+\]',item)
                        if dev:
                            mds_list[device_name]['active'].append(dev.group(1))
                            continue

                # handle missing metadata for raid0 array configurations.
                if raid_level == 'raid0':
                    active_total = len(mds_list[device_name]['active'])
                    failed_total = len(mds_list[device_name]['failed'])
                    spare_total = len(mds_list[device_name]['spare'])
                    total_devices = active_total + failed_total + spare_total
                    mds_list[device_name]['total'] = total_devices
                    mds_list[device_name]['up'] = active_total
                else:
                    # The next line should have some more array metadata.
                    detail = re.search('\[(\d+)\/(\d+)\]', f_mdstat.readline())
                    if detail:
                        mds_list[device_name]['total'] = detail.group(1)
                        mds_list[device_name]['up'] = detail.group(2)

                # There may or may not be a next line if a recovery is happening.
                mds_list[device_name]['recovery_speed'] = 0
                mds_list[device_name]['recovery_complete'] = 100
                recovery_line = f_mdstat.readline()
                if recovery_line.strip():
                    recovery = re.search('.*?(\d+\.?\d*).*?(\d+)K.*',recovery_line)
                    if recovery:
                        mds_list[device_name]['recovery_complete'] = recovery.group(1)
                        mds_list[device_name]['recovery_speed'] = recovery.group(2)
                else:
                    continue

        return mds_list