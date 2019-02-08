import lib.wl as wls
import sys
sys.path.append('./Lib')
import os
from utils import Color

color = Color()

class WeblogicWrapper:
    wlsObject = None
    STATUS_SHUTDOWN = "SHUTDOWN"
    STATUS_RUNNING = "RUNNING"
    TYPE_SERVER = 'Server'
    TYPE_CLUSTER = 'Cluster'

    originStdout = None

    def __init__(self, username=None, password=None, url=None, configFile=None, keyFile=None):
        if username is None and password is None:
            if configFile and keyFile:
                self.connect(configFile=configFile, keyFile=keyFile, url=url)
        else:
            self.connect(username=username, password=password, url=url)

    def __exit__(self):
        self.wlsObject.exit()

    def startRedirect(self):
        if self.originStdout == None:
            self.originStdout = sys.stdout
            sys.stdout = open('/dev/null', 'w')

    def stopRedirect(self):
        if self.originStdout != None:
            sys.stdout = self.originStdout

    def connect(self, username=None, password=None, url=None, configFile=None, keyFile=None):
        try:
            wls.redirect('/dev/null', 'false')
            if username is None and password is None and configFile and keyFile:
                wls.connect(userConfigFile=configFile,userKeyFile=keyFile, url=url)
            else:
                wls.connect(username, password, url)
            self.wlsObject = wls
            wls.stopRedirect()
        except:
            print "admin server not reachable"

    def getServer(self, serverName):
        try:
            self.wlsObject.domainConfig()
            origin = sys.stdout
            sys.stdout = open("/dev/null", "w")
            self.wlsObject.cd("/")
            servers = self.wlsObject.cmo.getServers()
            sys.stdout = origin
            for server in servers:
                if server.name == serverName:
                    return server
        except:
            return False

    def serverStatus(self, serverName):
        try:
            self.wlsObject.domainRuntime()
            slrBean = self.wlsObject.cmo.lookupServerLifeCycleRuntime(serverName)
            self.wlsObject.stopRedirect()
            return slrBean.getState()
        except:
            return "no server found"

    def serverStart(self, serverName):
        if self.serverStatus(serverName) != self.STATUS_RUNNING:
            try:
                print "starting server %s" % serverName
                self.wlsObject.start(serverName)
            except:
                print "error starting server %s" % serverName
                print self.wlsObject.dumpStack()
        else:
            print "server %s is already started" % serverName

    def serverStop(self, serverName, force=False):
        if self.serverStatus(serverName) != self.STATUS_SHUTDOWN:
            print "stopping server %s" % serverName
            try:
                self.wlsObject.shutdown(serverName, ignoreSessions='true', force=str(force).lower())
            except:
                pass
        else:
            print "server %s is already stopped" % serverName

    def getClusters(self):
        self.wlsObject.domainConfig()
        clusters = self.wlsObject.cmo.getClusters()
        return [x.name for x in clusters]


    def clusterExists(self, clusterName):
        return clusterName in self.getClusters()

    def getClusterMembers(self, clusterName):
        found = []
        if self.clusterExists(clusterName):
            self.wlsObject.domainConfig()
            self.wlsObject.cd('/Clusters/%s/Servers' % clusterName)
            servers = self.wlsObject.cmo.getServers()
            self.wlsObject.domainRuntime()
            self.wlsObject.cd('/')
            for server in servers:
                name = server.name
                if name != 'None' and name != None and name != '':
                    found.append(name)
        return found

    def clusterStatus(self, clusterName):
        if self.clusterExists(clusterName):
            servers = self.getClusterMembers(clusterName)
            if len(servers) == 0:
                print "no server found in cluster %s" % clusterName
            else:
                print "%-20s%-20s%-20s" % ( "Cluster", "Computer", "Status")
                print "-" * 60
                for server in servers:
                    status = self.serverStatus(server)
                    if status == self.STATUS_RUNNING: status = color.green(status)
                    elif status == self.STATUS_SHUTDOWN: status = color.red(status)
                    else: status = color.yellow(status)
                    print "%-20s%-20s%-20s" % ( clusterName, server, status )
        else:
            return False

    def __targetStop(self, targets, force=False):
        if ',' in targets:
            trgtLists = targets.split(',')
            for item in trgtLists:
                self.serverStop(item, force)
        else:
            self.serverStop(targets, force)

    def __targetStart(self, targets):
        if ',' in targets:
            for item in targets.split(','):
                self.serverStart(item)
        else:
            self.serverStart(targets)

    def getAppDeployments(self):
        self.startRedirect()
        #self.wlsObject.domainRuntime()
        appDeployments = self.wlsObject.cmo.getAppDeployments()
        self.stopRedirect()
        d = []
        for deployment in appDeployments:
            d.append(deployment.name)
        return d

    def getAppDeployment(self, deployName):
        deploys = self.getAppDeployments()
        for item in deploys:
            if item.startswith(deployName):
                return item
        return None

    def getAppDeploymentVersion(self, deployName):
        res = self.getAppDeployment(deployName)
        if res is not None:
            if '#' in res:
                return res.split('#')[-1]
            else:
                return "package %s doesn't have build version number" % deployName
        return "no deployment found for package %s" % deployName

    def undeployApp(self, appName, targets, cluster=False):
        if cluster:
            cluitem = self.getClusterMembers(targets)
            for item in cluitem:
                 self.__targetStop(item, force=True)
        else:
            self.__targetStop(targets, force=True)
        try:
            self.wlsObject.undeploy(appName)
        except:
            print "application %s is not deployed" % appName

    def deployApp(self, appName, package, targets, version=False, cluster=False):
        if cluster:
            cluitem = self.getClusterMembers(targets)
            for item in cluitem:
                self.__targetStop(item, force=True)
        else:
            self.__targetStop(targets, force=True)

        self.undeployApp(appName, targets)

        print "deploying package %s into app %s on targets %s" % ( package, appName, targets )
        if version:
            self.wlsObject.deploy(appName, package, upload='true', targets=targets, versionIdentifier=version)
        else:
            self.wlsObject.deploy(appName, package, upload='true', targets=targets)
        print "deploy complete. starting servers"
        if cluster:
            for item in self.getClusterMembers(targets):
                self.__targetStart(item)
        else:
            self.__targetStart(targets)
        print "server started"


