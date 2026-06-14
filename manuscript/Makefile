PDF=build/fhops-softx.pdf
TEX=fhops-softx.tex
BUILD_DIR=build
MANUSCRIPT_ROOT=$(abspath ..)
FHOPS_REPO?=$(abspath $(MANUSCRIPT_ROOT)/../fhops)
FHOPS_SOFTWAREX=$(FHOPS_REPO)/docs/softwarex
LOCAL_ASSETS=$(MANUSCRIPT_ROOT)/assets
EXTRAS_ASSETS=$(MANUSCRIPT_ROOT)/extras/assets
ASSET_SOURCE?=$(if $(wildcard $(LOCAL_ASSETS)),$(LOCAL_ASSETS),$(if $(wildcard $(EXTRAS_ASSETS)),$(EXTRAS_ASSETS),$(FHOPS_SOFTWAREX)/assets))
ELSARTICLE_DIR=elsarticle
ELSARTICLE_CLS=$(ELSARTICLE_DIR)/elsarticle.cls

export TEXINPUTS:=$(abspath $(ELSARTICLE_DIR))//:$(TEXINPUTS)
export BSTINPUTS:=$(abspath $(ELSARTICLE_DIR))//:$(BSTINPUTS)

.PHONY: all assets pdf clean default manuscript-benchmarks manuscript-benchmarks-fast

all: clean assets pdf

assets:
	install -D -m 0644 "$(ASSET_SOURCE)/data/tables/solver_performance.tex" "sections/includes/solver_performance.tex"
	install -D -m 0644 "$(ASSET_SOURCE)/data/tables/tuning_leaderboard.tex" "sections/includes/tuning_leaderboard.tex"
	install -D -m 0644 "$(ASSET_SOURCE)/data/playback/utilisation_robustness.png" "sections/includes/utilisation_robustness.png"
	install -D -m 0644 "$(ASSET_SOURCE)/data/scaling/runtime_vs_blocks.png" "sections/includes/runtime_vs_blocks.png"

manuscript-benchmarks:
	$(MAKE) -C "$(FHOPS_SOFTWAREX)/manuscript" manuscript-benchmarks
	$(MAKE) ASSET_SOURCE="$(FHOPS_SOFTWAREX)/assets" assets

manuscript-benchmarks-fast:
	$(MAKE) -C "$(FHOPS_SOFTWAREX)/manuscript" manuscript-benchmarks-fast
	$(MAKE) ASSET_SOURCE="$(FHOPS_SOFTWAREX)/assets" assets

pdf: $(PDF)

$(ELSARTICLE_CLS): $(ELSARTICLE_DIR)/elsarticle.ins $(ELSARTICLE_DIR)/elsarticle.dtx
	cd "$(ELSARTICLE_DIR)" && latex -interaction=nonstopmode elsarticle.ins

$(PDF): $(TEX) $(ELSARTICLE_CLS)
	mkdir -p $(BUILD_DIR)
	latexmk -pdf -interaction=nonstopmode -output-directory=$(BUILD_DIR) -auxdir=$(BUILD_DIR) $(TEX)

default: pdf

clean:
	latexmk -C -output-directory=$(BUILD_DIR) -auxdir=$(BUILD_DIR)
	$(RM) -r $(BUILD_DIR)
	$(RM) "$(ELSARTICLE_CLS)" "$(ELSARTICLE_DIR)/elsarticle.log"
