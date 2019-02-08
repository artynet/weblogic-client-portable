import sys
from lib.main import WeblogicWrapper
from lib.errors import Error
import config

def help():
    print """%s start|stop|status --cluster=WEBLOGIC_SERVER_NAME [--force]
    """ % sys.argv[0]
    sys.exit(-1)

def main():
    if len(sys.argv) <= 2:
        help()
    action = sys.argv[1].lower()
    if action in ('start','stop','status'):
        clusters = False
        try:
            clusterName = sys.argv[2].split("cluster=")[-1]
            wls = WeblogicWrapper(configFile=config.userConfigFile, keyFile=config.userKeyFile, url=config.url)
            if ',' in clusterName:
                clusters = clusterName.split(',')
            if action == 'start':
                if clusters:
                    for cluster in clusters:
                        for item in wls.getClusterMembers(cluster):
                            print wls.serverStart(item)
                else:
                    for item in wls.getClusterMembers(clusterName):
                        print wls.serverStart(item)
            elif action == 'stop':
                if len(sys.argv) > 3 and sys.argv[3] and sys.argv[3] == '--force':
                    force = True
                else:
                    force = True
                if clusters:
                    for cluster in clusters:
                        for item in wls.getClusterMembers(cluster):
                            wls.serverSop(item, force=True)
                else:
                    for item in wls.getClusterMembers(clusterName):
                        wls.serverStop(item, force=True)
            elif action == 'status':
                if clusters:
                    for cluster in clusters:
                        wls.clusterStatus(cluster)
                else:
                    wls.clusterStatus(clusterName)
            else:
                print "action %s not supported" % action
        except Exception, e:
            pass
    else:
        help()

main()
