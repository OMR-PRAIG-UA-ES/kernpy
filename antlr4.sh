rm -rf ../pykern/gen 2> /dev/null
rm -rf ../pykern/kern/generated 2> /dev/null

cd kern
java -jar ../antlr-4.13.1-complete.jar kernSpineLexer.g4 -Dlanguage=Python3 -o ../pykern/src/generated
cp ../pykern/src/generated/kernSpineLexer.tokens .
java -jar ../antlr-4.13.1-complete.jar -visitor kernSpineParser.g4 -Dlanguage=Python3 -o ../pykern/src/generated
java -jar ../antlr-4.13.1-complete.jar -listener kernSpineParser.g4 -Dlanguage=Python3 -o ../pykern/src/generated
