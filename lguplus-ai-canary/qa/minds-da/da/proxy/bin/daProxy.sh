#!/usr/bin/env bash
  PRG="$0"
  # Need this for relative symlinks.
  while [ -h "$PRG" ] ; do
      ls=`ls -ld "$PRG"`
      link=`expr "$ls" : '.*-> \(.*\)$'`
      if expr "$link" : '/.*' > /dev/null; then
          PRG="$link"
      else
          PRG=`dirname "$PRG"`"/$link"
      fi
  done
  SAVED="`pwd`"
  cd "`dirname \"$PRG\"`/../" >/dev/null
  APP_HOME="`pwd -P`"
  cd "$SAVED" >/dev/null
 
  APP_NAME="daProxy"
  APP_BASE_NAME=`basename "$0"`
 
  # Add default JVM options here. 
  DEFAULT_JVM_OPTS="-Xms512m -Xmx1024m -DpropertiesPath=${APP_HOME}/conf/proxy.properties"
 
  CLASSPATH=
 
  # Determine the Java command to use to start the JVM.
  if [ -n "$JAVA_HOME" ] ; then
      if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
          # IBM's JDK on AIX uses strange locations for the executables
          JAVACMD="$JAVA_HOME/jre/sh/java"
      else
          JAVACMD="$JAVA_HOME/bin/java"
      fi
      if [ ! -x "$JAVACMD" ] ; then
          die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME
 
  Please set the JAVA_HOME variable in your environment to match the
  location of your Java installation."
      fi
  else
      JAVACMD="java"
      which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
 
  Please set the JAVA_HOME variable in your environment to match the
  location of your Java installation."
  fi
 
exec "$JAVACMD" ${DEFAULT_JVM_OPTS} -jar $APP_HOME/lib/daProxy.jar "$@"
