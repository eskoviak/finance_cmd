PLANTUML_JAR := plantuml.jar
SRC_DIR       := .
OUT_DIR       := out

PUML_FILES := $(wildcard $(SRC_DIR)/*.puml)

.PHONY: all clean

all: $(OUT_DIR) $(PUML_FILES)
	java -jar $(PLANTUML_JAR) -tpng -o "$(abspath $(OUT_DIR))" $(PUML_FILES)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

clean:
	rm -rf $(OUT_DIR)
