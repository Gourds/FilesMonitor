# -*- coding: utf-8 -*-


import os
from threading import Timer
import time
import operator


class filesmonitor(object):
    _VersionRecord = []
    def __init__(self, path='.', interval=5, MaxRecord=2):
        self.path = str(path)
        self.interval = int(interval)
        self.MaxRecord = int(MaxRecord)

    def update_info(self):
        try:
            _total_dir,_total_file = ([],[])
            for r,d,f in os.walk(self.path, topdown=False):
                if d:
                    _total_dir += [os.path.join(r,dir) for dir in d]
                _total_file += [{'filename':os.path.join(r,name),'meta':self.meta_info(os.path.join(r,name))} for name in f]
            return(_total_dir, _total_file)
        except:
            pass

    def meta_info(self, filename):
        _rst = {}
        _rst['size'] = os.path.getsize(filename)
        _rst['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(os.path.getmtime(filename)))
        return(_rst)

    def check_modify(self):
        if filesmonitor._VersionRecord[-1][0] != filesmonitor._VersionRecord[-2][0]:
            return (False,'Directory has changed')
        if not operator.eq(filesmonitor._VersionRecord[-1][1], filesmonitor._VersionRecord[-2][1]):
            return (False, 'File has changed')
        return (True, 'no changed')
    def check(self):
        if len(filesmonitor._VersionRecord) < self.MaxRecord:
            filesmonitor._VersionRecord.append(self.update_info())
        else:
            del filesmonitor._VersionRecord[0:1]
            filesmonitor._VersionRecord.append(self.update_info())
            rst,msg = self.check_modify()
            if rst == False:
                self.function(*self.args, **self.kwargs)
        Timer(self.interval,self.check).start()

    def run(self,func,args=None, kwargs=None):
        self.function = func
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        Timer(self.interval,self.check).start()

if __name__ == '__main__':
    def my_function():
        print('hello world')
    a = filesmonitor(path='/Users/arvon/Documents/own-project/A-ops-scripts/ansible-playbook/other-scripts')
    a.run(my_function)
