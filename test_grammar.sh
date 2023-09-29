#!/bin/bash
JAR=antlr-4.13.0-complete.jar
TMP=/tmp/kerntest
if [ $# -lt 1 ]
then
    echo "Use: <input files>"
    exit 1
fi

mkdir ${TMP} 2> /dev/null
cp kern/*g4 ${TMP}

if [ ! -f ${TMP}/${JAR} ]; then
  cp ${JAR} ${TMP}
fi

cd ${TMP}
java -cp antlr-4.13.0-complete.jar org.antlr.v4.Tool kernLexer.g4
java -cp antlr-4.13.0-complete.jar org.antlr.v4.Tool kernParser.g4
javac -cp antlr-4.13.0-complete.jar *java
cd -
java -cp ${TMP}:antlr-4.13.0-complete.jar org.antlr.v4.gui.TestRig kern start $*
