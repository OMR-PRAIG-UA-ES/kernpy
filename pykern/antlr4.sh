rm -rf gen 2> /dev/null
rm -rf generated/kern 2> /dev/null
#java -jar ./antlr-4.13.1-complete.jar kern/kernLexer.g4 -Dlanguage=Python3 -o src/generated
#cp src/generated/kern/kernLexer.tokens kern
#java -jar ./antlr-4.13.1-complete.jar -visitor kern/kernParser.g4 -Dlanguage=Python3 -o src/generated
#java -jar ./antlr-4.13.1-complete.jar -listener kern/kernParser.g4 -Dlanguage=Python3 -o src/generated

cd kern
java -jar ../antlr-4.13.1-complete.jar kernSpineLexer.g4 -Dlanguage=Python3 -o generated
cp ../src/generated/kernSpineLexer.tokens .
java -jar ../antlr-4.13.1-complete.jar -visitor kernSpineParser.g4 -Dlanguage=Python3 -o generated
java -jar ../antlr-4.13.1-complete.jar -listener kernSpineParser.g4 -Dlanguage=Python3 -o generated
