#Author: Alex Li
import sys,os

basedir = '/'.join(__file__.split("/")[:-2])
sys.path.append(basedir)

sys.path.append('%s/MonitorServer' %basedir)
os.environ['DJANGO_SETTINGS_MODULE'] ='MonitorServer.settings'
import django
django.setup()

'''#for windows platform only
cur_dir = os.path.split(os.path.abspath(__file__))[0].split('\\')[:-1]
base_dir = '\\'.join(cur_dir)
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auto_cmdb.settings")
'''

#from web import models
#print models.Hosts.objects.all()

