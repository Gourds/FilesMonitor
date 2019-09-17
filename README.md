
### 简介

监控目录是否产生变化，如果产生变化就执行某个自定义任务

### 使用

```python
from FilesMonitor import filesmonitor

def example_job():
    print('hello world')

foo = filesmonitor(path='/your/path',interval=5)
foo.run(example_job)
```
