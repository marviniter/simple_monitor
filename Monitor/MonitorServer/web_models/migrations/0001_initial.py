# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_type', models.IntegerField(default=0, choices=[(0, b'CMD'), (1, b'Login'), (2, b'Logout'), (3, b'GetFile'), (4, b'SendFile'), (5, b'exception')])),
                ('cmd', models.TextField()),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name': '\u5ba1\u8ba1\u65e5\u5fd7',
                'verbose_name_plural': '\u5ba1\u8ba1\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='BindHosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4e0e\u8fdc\u7a0b\u7528\u6237\u7ed1\u5b9a',
                'verbose_name_plural': '\u4e3b\u673a\u8fdc\u7a0b\u4e0e\u7528\u6237\u7ed1\u5b9a',
            },
        ),
        migrations.CreateModel(
            name='Conditions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('data_type', models.CharField(default=b'char', max_length=32, verbose_name='\u6570\u636e\u7c7b\u578b')),
                ('threshold', models.CharField(max_length=64, verbose_name='\u9600\u503c')),
            ],
            options={
                'verbose_name': '\u9600\u503c',
                'verbose_name_plural': '\u9600\u503c',
            },
        ),
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nice', models.CharField(max_length=64)),
                ('system', models.CharField(max_length=64)),
                ('iowait', models.CharField(max_length=64)),
                ('steal', models.CharField(max_length=64)),
                ('idle', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'CPU',
                'verbose_name_plural': 'CPU',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
            options={
                'verbose_name': '\u90e8\u95e8',
                'verbose_name_plural': '\u90e8\u95e8',
            },
        ),
        migrations.CreateModel(
            name='Formulas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('key', models.CharField(unique=True, max_length=64)),
                ('memo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HostGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u7ec4',
                'verbose_name_plural': '\u4e3b\u673a\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=64)),
                ('ip_addr', models.GenericIPAddressField(unique=True)),
                ('system_type', models.CharField(default=b'linux', max_length=32, choices=[(b'windows', b'Windows'), (b'linux', b'Linux/Unix')])),
                ('port', models.IntegerField(default=22)),
                ('enabled', models.BooleanField(default=True, help_text='\u4e3b\u673a\u82e5\u4e0d\u60f3\u88ab\u7528\u6237\u8bbf\u95ee\u53ef\u4ee5\u53bb\u6389\u6b64\u9009\u9879')),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='web_models.HostGroups')),
            ],
            options={
                'verbose_name': '\u4e3b\u673a',
                'verbose_name_plural': '\u4e3b\u673a',
            },
        ),
        migrations.CreateModel(
            name='HostUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_method', models.CharField(help_text='\u5982\u679c\u9009\u62e9SSH/KEY\uff0c\u8bf7\u786e\u4fdd\u4f60\u7684\u79c1\u94a5\u6587\u4ef6\u5df2\u5728settings.py\u4e2d\u6307\u5b9a', max_length=16, choices=[(b'ssh-password', b'SSH/Password'), (b'ssh-key', b'SSH/KEY')])),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(help_text='\u5982\u679cauth_method\u9009\u62e9\u7684\u662fSSH/KEY,\u90a3\u6b64\u5904\u4e0d\u9700\u8981\u586b\u5199..', max_length=64, null=True, blank=True)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u8fdc\u7a0b\u7528\u6237',
                'verbose_name_plural': '\u8fdc\u7a0b\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
            options={
                'verbose_name': 'IDC',
                'verbose_name_plural': 'IDC',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('key', models.CharField(max_length=100)),
                ('data_type', models.CharField(max_length=50, choices=[(b'float', b'Float'), (b'string', b'String'), (b'integer', b'Integer')])),
                ('unit', models.CharField(default=b'%', max_length=30)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u76d1\u63a7\u9879',
                'verbose_name_plural': '\u76d1\u63a7\u9879',
            },
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('MemTotal', models.CharField(max_length=64)),
                ('MemUsage', models.CharField(max_length=64)),
                ('Cached', models.CharField(max_length=64)),
                ('MemFree', models.CharField(max_length=64)),
                ('Buffers', models.CharField(max_length=64)),
                ('SwapFree', models.CharField(max_length=64)),
                ('SwapTotal', models.CharField(max_length=64)),
                ('host', models.ForeignKey(to='web_models.Hosts')),
            ],
            options={
                'verbose_name': '\u5185\u5b58',
                'verbose_name_plural': '\u5185\u5b58',
            },
        ),
        migrations.CreateModel(
            name='Operators',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('key', models.CharField(max_length=32)),
                ('memo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monitor_type', models.CharField(max_length=50, choices=[(b'agent', b'Agent'), (b'snmp', b'Snmp'), (b'wget', b'Wget')])),
                ('name', models.CharField(unique=True, max_length=50)),
                ('plugin', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '\u670d\u52a1',
                'verbose_name_plural': '\u670d\u52a1',
            },
        ),
        migrations.CreateModel(
            name='ServiceTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('key', models.CharField(max_length=50)),
                ('check_interval', models.IntegerField(default=300)),
                ('description', models.TextField()),
                ('conditions', models.ManyToManyField(to='web_models.Conditions', verbose_name=b'\xe9\x98\x80\xe5\x80\xbc\xe5\x88\x97\xe8\xa1\xa8')),
                ('service', models.ForeignKey(to='web_models.Services')),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u6a21\u677f',
                'verbose_name_plural': '\u670d\u52a1\u6a21\u677f',
            },
        ),
        migrations.CreateModel(
            name='SessionTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('closed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=64)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire', models.IntegerField(default=300)),
                ('host', models.ForeignKey(to='web_models.BindHosts')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('host_group', models.ManyToManyField(to='web_models.HostGroups')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u7ec4',
                'verbose_name_plural': '\u7528\u6237\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('valid_begin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_end_time', models.DateTimeField()),
                ('bind_hosts', models.ManyToManyField(to='web_models.BindHosts', verbose_name='\u6388\u6743\u4e3b\u673a', blank=True)),
                ('department', models.ForeignKey(verbose_name='\u90e8\u95e8', to='web_models.Department')),
                ('host_groups', models.ManyToManyField(to='web_models.HostGroups', verbose_name='\u6388\u6743\u4e3b\u673a\u7ec4', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u8fd0\u7ef4\u5e73\u53f0\u8d26\u6237',
                'verbose_name_plural': '\u8fd0\u7ef4\u5e73\u53f0\u8d26\u6237',
            },
        ),
        migrations.AddField(
            model_name='usergroup',
            name='user_info',
            field=models.ManyToManyField(to='web_models.UserProfile'),
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.ForeignKey(to='web_models.UserProfile'),
        ),
        migrations.AddField(
            model_name='items',
            name='service',
            field=models.ForeignKey(to='web_models.Services'),
        ),
        migrations.AlterUniqueTogether(
            name='hostusers',
            unique_together=set([('auth_method', 'password', 'username')]),
        ),
        migrations.AddField(
            model_name='hosts',
            name='idc',
            field=models.ForeignKey(to='web_models.IDC'),
        ),
        migrations.AddField(
            model_name='hostgroups',
            name='service_template',
            field=models.ManyToManyField(to='web_models.ServiceTemplate'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='host',
            field=models.ForeignKey(to='web_models.Hosts'),
        ),
        migrations.AddField(
            model_name='conditions',
            name='formula',
            field=models.ForeignKey(verbose_name='\u8fd0\u7b97\u51fd\u6570', to='web_models.Formulas'),
        ),
        migrations.AddField(
            model_name='conditions',
            name='item',
            field=models.ForeignKey(verbose_name='\u76d1\u63a7\u503c', to='web_models.Items'),
        ),
        migrations.AddField(
            model_name='conditions',
            name='operator',
            field=models.ForeignKey(verbose_name='\u8fd0\u7b97\u7b26', blank=True, to='web_models.Operators', null=True),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host',
            field=models.ForeignKey(to='web_models.Hosts'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_group',
            field=models.ManyToManyField(to='web_models.HostGroups'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_user',
            field=models.ForeignKey(to='web_models.HostUsers'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='host',
            field=models.ForeignKey(to='web_models.BindHosts'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='session',
            field=models.ForeignKey(to='web_models.SessionTrack'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(to='web_models.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhosts',
            unique_together=set([('host', 'host_user')]),
        ),
    ]
