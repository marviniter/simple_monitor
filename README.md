# simple_monitor

#云平台域名功能规划

##要解决的问题
```
1.kubernetes中service名称到service_ip的解析
2.应用访问地址到活动状态节点的ip解析
3.常规的DNS服务提供
```



###问题1解决方案：
###集成SkyDns与Kube2Sky到云平台中，使用云平台的etcd作为后端存储。由Kube2Sky动态发现服务并生成配置信息存放到etcd中，SkyDns读取配置信息。

###问题2的解决方案
###

```flow
st=>start: Start
e=>end: End
op1=>operation: My Operation
sub1=>subroutine: My Subroutine
cond=>condition: Yes or No?
io=>inputoutput: catch something...
st->op1->cond
cond(yes)->io->e
cond(no)->sub1(right)->op1
```

```sequence
Alice->Bob: Hello Bob, how are you?
Note right of Bob: Bob thinks
Bob-->Alice: I am good thanks!
```



