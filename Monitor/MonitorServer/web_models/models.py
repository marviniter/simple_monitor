#_*_coding:utf-8_*_
from django.db import models
import django
from django.contrib.auth.models import User
import datetime
# Create your models here.

class IDC(models.Model):
    name = models.CharField(max_length=64,unique=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'IDC'
        verbose_name_plural = u'IDC'

class Department(models.Model):
    name = models.CharField(max_length=64,unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'部门'
        verbose_name_plural = u'部门'

class Hosts(models.Model):
    hostname = models.CharField(max_length=64,unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    system_type_choices = (
        ('windows','Windows'),
        ('linux', 'Linux/Unix')
    )
    idc = models.ForeignKey('IDC')
    group = models.ForeignKey('HostGroups')
    system_type = models.CharField(choices=system_type_choices,max_length=32,default='linux')
    port = models.IntegerField(default=22)
    enabled = models.BooleanField(default=True,help_text=u'主机若不想被用户访问可以去掉此选项')
    #host_users = models.ForeignKey('HostUsers')
    #host_groups = models.ForeignKey('HostGroups')
    memo = models.CharField(max_length=128,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s(%s)' %(self.hostname,self.ip_addr)
    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u'主机'
        
class HostUsers(models.Model):
    auth_method_choices = (('ssh-password',"SSH/Password"),('ssh-key',"SSH/KEY"))
    auth_method = models.CharField(choices=auth_method_choices,max_length=16,help_text=u'如果选择SSH/KEY，请确保你的私钥文件已在settings.py中指定')
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64,blank=True,null=True,help_text=u'如果auth_method选择的是SSH/KEY,那此处不需要填写..')
    memo = models.CharField(max_length=128,blank=True,null=True)
    def __unicode__(self):
        return '%s(%s)' %(self.username,self.password)
    class Meta:
        verbose_name = u'远程用户'
        verbose_name_plural = u'远程用户'
        unique_together = ('auth_method','password','username')

class BindHosts(models.Model):
    host = models.ForeignKey('Hosts')
    host_user = models.ForeignKey('HostUsers')
    host_group = models.ManyToManyField('HostGroups')
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s:%s' %(self.host.hostname,self.host_user.username)
    class Meta:
        unique_together = ("host", "host_user")
        verbose_name = u'主机与远程用户绑定'
        verbose_name_plural = u'主机远程与用户绑定'
    def get_groups(self):
            return ",\n".join([g.name for g in self.host_group.all()])

class HostGroups(models.Model):
    name = models.CharField(max_length=64,unique=True)
    memo = models.CharField(max_length=128,blank=True,null=True)
    service_template = models.ManyToManyField('ServiceTemplate')

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = u'主机组'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(unique=True,max_length=32)
    department = models.ForeignKey('Department',verbose_name=u'部门')
    #user_groups = models.ManyToManyField('PUserGroups') #might use it in the future version
    host_groups = models.ManyToManyField('HostGroups',verbose_name=u'授权主机组',blank=True)
    bind_hosts = models.ManyToManyField('BindHosts',verbose_name=u'授权主机',blank=True)
    valid_begin_time = models.DateTimeField(default=django.utils.timezone.now)
    valid_end_time = models.DateTimeField()

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'运维平台账户'
        verbose_name_plural = u'运维平台账户'

class SessionTrack(models.Model):

    date = models.DateTimeField(default=django.utils.timezone.now)
    closed = models.BooleanField(default=False)
    def __unicode__(self):
        return '%s' %self.id

class AuditLog(models.Model):
    session = models.ForeignKey(SessionTrack)
    user = models.ForeignKey('UserProfile')
    host = models.ForeignKey('BindHosts')
    action_choices = (
        (0,'CMD'),
        (1,'Login'),
        (2,'Logout'),
        (3,'GetFile'),
        (4,'SendFile'),
        (5,'exception'),
    )
    action_type = models.IntegerField(choices=action_choices,default=0)
    cmd = models.TextField()
    memo = models.CharField(max_length=128,blank=True,null=True)
    date = models.DateTimeField()


    def __unicode__(self):
        return '%s-->%s@%s:%s' %(self.user.user.username,self.host.host_user.username,self.host.host.ip_addr,self.cmd)
    class Meta:
        verbose_name = u'审计日志'
        verbose_name_plural = u'审计日志'


class Token(models.Model):
    user = models.ForeignKey(UserProfile)
    host = models.ForeignKey(BindHosts)
    token = models.CharField(max_length=64)
    date = models.DateTimeField(default=django.utils.timezone.now)
    expire = models.IntegerField(default=300)

    def __unicode__(self):
        return '%s : %s' %(self.host.host.ip_addr,self.token)

#监控项
class Items(models.Model):
    #可自定义
    name = models.CharField(max_length=50,)
    #与client中收集数据字典(value_dic)的key相同
    key = models.CharField(max_length=100,)
    #监控项的数据类型
    data_type_option = (("float","Float"),('string','String'),('integer','Integer'))
    data_type = models.CharField(max_length=50,choices=data_type_option)
    unit = models.CharField(max_length=30,default='%')
    #监控项是否启用，一般不用
    enabled = models.BooleanField(default=True)
    
    #一个server对应多个item,item-->server 为多对一关系
    service = models.ForeignKey('Services')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'监控项'
        verbose_name_plural = u'监控项'

#一个服务模板属于一个服务，一个服务可包含多个模板      
class Services(models.Model):
    monitor_type_list = (('agent','Agent'),('snmp','Snmp'),('wget','Wget'))
    monitor_type = models.CharField(max_length=50,choices=monitor_type_list)
    #服务名
    name = models.CharField(max_length=50,unique=True)
    #插件名,与Client(plugin_api模块)中定义的插件名称一致
    plugin = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'服务'
        verbose_name_plural = u'服务'
        
#定义服务模板，例如:同一监控服务的监控间隔，阀值不同(cpu1,cpu2,memory1,memory2...)
class ServiceTemplate(models.Model):
    #name为自定义
    name = models.CharField(max_length=50,unique=True)
    
    #key为收集配置数据字典的key，cpu，memory，load
    key =  models.CharField(max_length=50)
    #执行间隔时间
    check_interval = models.IntegerField(default=300)
    #ServiceTemplate-->Service 多对一关系
    #cpu1,cpu2,cpu3 --> cup
    service = models.ForeignKey('Services')
    
    #阀值,service-->conditions为多对多关系，一个item对应一个阀值
    #单个阀值与item的关系为多对一的关系
    conditions = models.ManyToManyField('Conditions',verbose_name='阀值列表')
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'服务模板'
        verbose_name_plural = u'服务模板'
          
class Formulas(models.Model):
    name = models.CharField(max_length=64,unique=True)
    key = models.CharField(max_length=64,unique=True)
    memo = models.TextField()
    
    def __unicode__(self):
        return self.name
    
  
class Operators(models.Model):
    name = models.CharField(max_length=32,unique=True)
    key = models.CharField(max_length=32)
    memo = models.TextField()
    
    def __unicode__(self):
        return self.name

#定义阀值表达式 <num >num =num
class Conditions(models.Model):
    name = models.CharField(max_length=100,unique=True)
    #condition与item做多对一的关系
    item = models.ForeignKey('Items',verbose_name=u'监控值')
    #定义函数，avg(求平均值)，sum(求和)
    formula = models.ForeignKey('Formulas',verbose_name=u'运算函数')
    
    #定义操作，可以通过反射执行，函数名:gt 表示大于，lt 表示小于，max，min，abs
    operator = models.ForeignKey('Operators',verbose_name=u'运算符',null=True,blank=True)
    data_type = models.CharField(default='char',max_length=32,verbose_name=u'数据类型')
    threshold = models.CharField(max_length=64,verbose_name=u'阀值')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'阀值'
        verbose_name_plural = u'阀值'
    
#用户组与主机组为多对多关系       
class UserGroup(models.Model):
    name = models.CharField(max_length=50,unique=True)
    host_group = models.ManyToManyField('HostGroups')
    user_info = models.ManyToManyField('UserProfile')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'用户组'
        verbose_name_plural = u'用户组'
    
        
class Cpu(models.Model):
    host = models.ForeignKey('Hosts')
    clock = models.CharField(max_length=64)
    
    nice = models.CharField(max_length=64)
    system = models.CharField(max_length=64)
    iowait = models.CharField(max_length=64)
    steal = models.CharField(max_length=64)
    idle = models.CharField(max_length=64)
    
    def __unicode__(self):
        return 'CPU'
	
    class Meta:
        verbose_name = u'CPU'
        verbose_name_plural = u'CPU'
        
class Memory(models.Model):
    host = models.ForeignKey('Hosts')
    clock = models.CharField(max_length=64)

    MemTotal = models.CharField(max_length=64)
    MemUsage = models.CharField(max_length=64)
    Cached = models.CharField(max_length=64)
    MemFree = models.CharField(max_length=64)
    Buffers = models.CharField(max_length=64)
    SwapFree = models.CharField(max_length=64)
    SwapTotal = models.CharField(max_length=64)
    
    def __unicode__(self):
        return "Memory"
	
    class Meta:
        verbose_name = u'内存'
        verbose_name_plural = u'内存'

