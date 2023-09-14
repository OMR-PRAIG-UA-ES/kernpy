java -jar ./antlr-4.13.0-complete.jar grammar/kernLexer.g4 -Dlanguage=Python3 -o src/generated/antlr
cp src/generated/antlr/grammar/kernLexer.tokens grammar
java -jar ./antlr-4.13.0-complete.jar -visitor grammar/kernParser.g4  -Dlanguage=Python3 -o src/generated/antlr
