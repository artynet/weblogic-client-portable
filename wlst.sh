#!/bin/bash
CP=$(echo lib/*.jar | tr ' ' ':')
WLS_HOME=$(pwd)
WLST_HOME=$WLS_HOME
WLST_PROPERTIES="-Dbea.home=$(pwd) -Dweblogic.home=$(pwd) -Dwlst.offline.log=disable"
WL_PRODUCT_FILE="${WLS_HOME}/resources/.product.properties"
WLS_NOT_BRIEF_ENV=true
[[ ! -f $WL_PRODUCT_FILE ]] && touch $WL_PRODUCT_FILE
JVM_ARGS="-Dprod.props.file=${WL_PRODUCT_FILE} ${WLST_PROPERTIES} -cp $CP"


java ${JVM_ARGS} weblogic.WLST $@  | sed -e "1,8 d"
#java ${JVM_ARGS} weblogic.WLST $@ 
#eval 'java' ${JVM_ARGS} weblogic.WLST $@
exit ${PIPESTATUS[0]}

