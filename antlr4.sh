rm -rf kernpy/gen 2> /dev/null
rm -rf kernpy/core/generated 2> /dev/null

cd kern
java -jar ../antlr-4.13.1-complete.jar kernSpineLexer.g4 -Dlanguage=Python3 -o ../kernpy/core/generated
cp ../kernpy/core/generated/kernSpineLexer.tokens .
java -jar ../antlr-4.13.1-complete.jar -visitor kernSpineParser.g4 -Dlanguage=Python3 -o ../kernpy/core/generated
java -jar ../antlr-4.13.1-complete.jar -listener kernSpineParser.g4 -Dlanguage=Python3 -o ../kernpy/core/generated
cp ../kernpy/core/generated/kernSpineParser.tokens .

# **mens: the combined **kern/**mens grammar, vendored verbatim from mOOsicae (antlr/humdrum/).
# Never edit kernMensSpine*.g4 here: change them in mOOsicae and copy them back (see kern/README-mens.md).
java -jar ../antlr-4.13.1-complete.jar kernMensSpineLexer.g4 -Dlanguage=Python3 -o ../kernpy/core/generated
cp ../kernpy/core/generated/kernMensSpineLexer.tokens .
java -jar ../antlr-4.13.1-complete.jar -visitor -listener kernMensSpineParser.g4 -Dlanguage=Python3 -o ../kernpy/core/generated
cp ../kernpy/core/generated/kernMensSpineParser.tokens .
