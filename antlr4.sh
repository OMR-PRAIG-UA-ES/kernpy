rm -rf gen 2> /dev/null
java -jar ./antlr-4.13.0-complete.jar kern/kernLexer.g4 -Dlanguage=Python3 -o src/generated
cp src/generated/kern/kernLexer.tokens kern
java -jar ./antlr-4.13.0-complete.jar -visitor kern/kernParser.g4  -Dlanguage=Python3 -o src/generated
