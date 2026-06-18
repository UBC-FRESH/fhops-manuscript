PDF=build/fhops-softx.pdf
TEX=fhops-softx.tex
BUILD_DIR=build
SUBMISSION_NAME=fhops-softx-em-flat
SUBMISSION_DIR=$(BUILD_DIR)/$(SUBMISSION_NAME)
SUBMISSION_ZIP=$(BUILD_DIR)/$(SUBMISSION_NAME).zip
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

.PHONY: all assets pdf submission-package clean default manuscript-benchmarks manuscript-benchmarks-fast

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

submission-package: all
	$(RM) -r "$(SUBMISSION_DIR)" "$(SUBMISSION_ZIP)"
	install -d "$(SUBMISSION_DIR)"
	install -m 0644 "$(TEX)" references.bib "$(SUBMISSION_DIR)/"
	install -m 0644 metadata/code_metadata.tex metadata/current_code_version.tex "$(SUBMISSION_DIR)/"
	install -m 0644 sections/highlights.tex sections/abstract.tex sections/introduction.tex "$(SUBMISSION_DIR)/"
	install -m 0644 sections/software_description.tex sections/illustrative_example.tex "$(SUBMISSION_DIR)/"
	install -m 0644 sections/impact.tex sections/conclusions.tex sections/acknowledgments.tex "$(SUBMISSION_DIR)/"
	install -m 0644 sections/includes/fhops_operational_formulation.tex "$(SUBMISSION_DIR)/"
	install -m 0644 sections/includes/solver_performance.tex sections/includes/tuning_leaderboard.tex "$(SUBMISSION_DIR)/"
	install -m 0644 sections/includes/utilisation_robustness.png sections/includes/runtime_vs_blocks.png "$(SUBMISSION_DIR)/"
	install -m 0644 "$(ELSARTICLE_CLS)" "$(ELSARTICLE_DIR)/elsarticle-num.bst" "$(SUBMISSION_DIR)/"
	perl -0pi -e 's/\{sections\/(highlights|abstract|introduction|software_description|illustrative_example|impact|conclusions|acknowledgments)\}/{$$1}/g; s/\{metadata\/(code_metadata|current_code_version)\}/{$$1}/g; s/\{sections\/includes\/fhops_operational_formulation\}/{fhops_operational_formulation}/g; s/\{sections\/includes\/solver_performance\.tex\}/{solver_performance.tex}/g; s/\{sections\/includes\/tuning_leaderboard\.tex\}/{tuning_leaderboard.tex}/g; s/\{sections\/includes\/utilisation_robustness\.png\}/{utilisation_robustness.png}/g; s/\{sections\/includes\/runtime_vs_blocks\.png\}/{runtime_vs_blocks.png}/g' "$(SUBMISSION_DIR)"/*.tex
	cd "$(SUBMISSION_DIR)" && zip -q "../$(SUBMISSION_NAME).zip" *
	@printf 'Wrote %s\n' "$(SUBMISSION_ZIP)"

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
