import sys
from lib.main import WeblogicWrapper
from lib.utils import getOpt
import config

def help():
    print """%s start|stop|status --server=WEBLOGIC_SERVER_NAME [--force]
    """ % sys.argv[0]
    sys.exit(-1)

def main():
    if len(sys.argv) <= 2:
        help()
    argv = sys.argv
    scriptName = argv.pop(0)
    action = argv.pop(0).lower()
    server, force = (None, None)
    for args in argv:
        if server is None:
            server = getOpt("--server=", args)
        if force is None:
            force = getOpt("--force=", args)

    if action in ('start','stop','status') and server:
        servers = False
        try:
            serverName = server
            wls = WeblogicWrapper(configFile=config.userConfigFile, keyFile=config.userKeyFile, url=config.url)
            if ',' in serverName:
                servers = serverName.split(',')

            if action == 'start':
                if servers:
                    res = [wls.serverStart(x) for x in servers]
                    print res
                else:
                    wls.serverStart(serverName)
            elif action == 'stop':
                if servers:
                    res = [wls.serverStop(x) for x in servers]
                    print res
                else:
                    wls.serverStop(serverName, force=force)
            elif action == 'status':
                if servers:
                    for res in [(x, wls.serverStatus(x)) for x in servers]:
                        print "%s - %s" % (res[0], res[1])
                else:
                    state = wls.serverStatus(serverName)
                    print state
            else:
                print "action %s not supported" % action
        except Exception, e:
            print e

main()
