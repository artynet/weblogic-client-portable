import config



def help():
    print """%s deploy|undeploy|get-version
    --name=WEBLOGIC_SERVER_NAME                 servername
    --package=PATH_OF_PACKAGE                   /tmp/package.ear
    --target=TARGET                             server1,server2
    """ % sys.argv[0]
    sys.exit(-1)

def main():

    if len(sys.argv) <= 2:
        help()
    argv = sys.argv
    print   # fix buffer bug
    scriptName = argv.pop(0)
    action = argv.pop(0).lower()

    name, package, target, version, cluster = (None, None, None, None, None)
    print argv

    for args in argv:
        if name is None:
            name = getOpt("--name=", args)
        if package is None:
            package = getOpt("--package=", args)
        if target is None:
            target = getOpt("--targets=", args)
        if version is None:
            version = getOpt("--version=", args)
        if cluster is None or not cluster:
            cluster = "--cluster" in args

    if name:
        wls = WeblogicWrapper(configFile=config.userConfigFile, keyFile=config.userKeyFile, url=config.url)

    if action == 'deploy' and name and package and target:
        if version:
            wls.deployApp(name, package, target, getVersion(version))
        else:
            try:
                wls.deployApp(name, package, target, cluster=cluster)
            except:
                print "deploy error"

    elif action == 'undeploy' and name and target:
        wls.undeployApp(name, target, cluster=cluster)
    elif action == 'get-version' and name:
        print wls.getAppDeploymentVersion(name)
    else:
        help()

main()

