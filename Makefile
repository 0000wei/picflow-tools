PROJ_ROOT := $(shell pwd)

# ── Tool dirs: exclude reserved/auxiliary directories ─────────────────────────
RESERVED := zh ja de fr es pt ar css js images config docs scripts seo .git __pycache__ node_modules
# Compute tool directories: everything under root that is a directory AND not in RESERVED
TOOL_DIRS := $(shell cd "$(PROJ_ROOT)" && for d in */; do \
  d=$${d%/}; \
  skip=0; \
  for r in $(RESERVED); do [ "$$d" = "$$r" ] && skip=1; done; \
  [ $$skip -eq 0 ] && echo "$$d"; \
  done)

# ── EN-only directories (NOT expected in lang mirror) ──────────────────────────
EN_ONLY := avif-to-png

# ── Language directories ──────────────────────────────────────────────────────
LANG_DIRS := zh ja de fr es pt ar

# ==============================================================================
# verify — project integrity checks
# ==============================================================================
.PHONY: verify
verify: verify-tool-indexes verify-lang-mirror verify-seo-files verify-config-files verify-root-files
	@echo ""
	@echo "✓ All verify checks passed."

# 1. Every tool dir must contain index.html
.PHONY: verify-tool-indexes
verify-tool-indexes:
	@echo "── Tool directory index.html check ──"
	@missing=""; \
	for d in $(TOOL_DIRS); do \
	  if [ ! -f "$(PROJ_ROOT)/$$d/index.html" ]; then \
	    missing="$$missing  ✗ $$d/index.html\n"; \
	  fi; \
	done; \
	if [ -n "$$missing" ]; then \
	  printf "FAIL: Missing index.html in tool directories:\n$$missing"; \
	  exit 1; \
	fi; \
	echo "  ✓ All $(words $(TOOL_DIRS)) tool directories have index.html"

# 2. Language dirs mirror tool directory structure
.PHONY: verify-lang-mirror
verify-lang-mirror:
	@echo "── Language directory mirror check ──"
	@error=0; \
	for lang in $(LANG_DIRS); do \
	  mismatch=""; \
	  for d in $(TOOL_DIRS); do \
	    skip=0; \
	    for e in $(EN_ONLY); do [ "$$d" = "$$e" ] && skip=1; done; \
	    [ $$skip -eq 1 ] && continue; \
	    if [ ! -d "$(PROJ_ROOT)/$$lang/$$d" ]; then \
	      mismatch="$$mismatch  ✗ $$lang/$$d (missing)\n"; \
	    fi; \
	  done; \
	  if [ -n "$$mismatch" ]; then \
	    echo "  FAIL: $$lang directory structure differs:"; \
	    printf "$$mismatch"; \
	    error=1; \
	  else \
	    echo "  ✓ $$lang — complete mirror"; \
	  fi; \
	done; \
	if [ "$$error" -ne 0 ]; then exit 1; fi

# 3. SEO files exist
.PHONY: verify-seo-files
verify-seo-files:
	@echo "── SEO files check ──"
	@ok=1; \
	for f in sitemap.xml robots.txt; do \
	  if [ -f "$(PROJ_ROOT)/seo/$$f" ]; then \
	    echo "  ✓ seo/$$f"; \
	  else \
	    echo "  ✗ seo/$$f MISSING"; \
	    ok=0; \
	  fi; \
	done; \
	[ "$$ok" -eq 1 ] || (echo "FAIL: SEO files incomplete"; exit 1)

# 4. Config / root files
.PHONY: verify-config-files
verify-config-files:
	@echo "── Config file check ──"
	@error=0; \
	\
	cfg="$(PROJ_ROOT)/config/mcp.json"; \
	if [ -f "$$cfg" ]; then \
	  echo "  ✓ config/mcp.json"; \
	  python3 -c "import json; json.load(open('$$cfg'))" 2>/dev/null && \
	    echo "    → valid JSON" || (echo "    → INVALID JSON"; error=1); \
	else \
	  echo "  ✗ config/mcp.json MISSING"; error=1; \
	fi; \
	\
	vc="$(PROJ_ROOT)/vercel.json"; \
	if [ -f "$$vc" ]; then \
	  echo "  ✓ vercel.json"; \
	  python3 -c "import json; json.load(open('$$vc'))" 2>/dev/null && \
	    echo "    → valid JSON" || (echo "    → INVALID JSON"; error=1); \
	else \
	  echo "  ✗ vercel.json MISSING"; error=1; \
	fi; \
	\
	[ "$$error" -eq 0 ] || (echo "FAIL: Config files have issues"; exit 1)

.PHONY: verify-root-files
verify-root-files:
	@echo "── Root required files check ──"
	@error=0; \
	for f in README.md AGENTS.md; do \
	  if [ -f "$(PROJ_ROOT)/$$f" ]; then \
	    echo "  ✓ $$f"; \
	  else \
	    echo "  ✗ $$f MISSING"; \
	    error=1; \
	  fi; \
	done; \
	[ "$$error" -eq 0 ] || (echo "FAIL: Required root files missing"; exit 1)

# ==============================================================================
# lint — code quality checks
# ==============================================================================
.PHONY: lint
lint: lint-gitignore lint-root-files
	@echo ""
	@echo "✓ All lint checks passed."

.PHONY: lint-gitignore
lint-gitignore:
	@echo "── .gitignore coverage check ──"
	@gi="$(PROJ_ROOT)/.gitignore"; \
	error=0; \
	for pattern in "__pycache__" ".well-known"; do \
	  if grep -q "$$pattern" "$$gi" 2>/dev/null; then \
	    echo "  ✓ .gitignore covers $$pattern"; \
	  else \
	    echo "  ✗ .gitignore does NOT cover $$pattern"; \
	    error=1; \
	  fi; \
	done; \
	[ "$$error" -eq 0 ] || (echo "FAIL: .gitignore is incomplete"; exit 1)

.PHONY: lint-root-files
lint-root-files:
	@echo "── Root file allowlist check ──"
	@ALLOWED_FILES="STRUCTURE-RULES.md AGENTS.md README.md .gitignore vercel.json Makefile PROGRESS.md feature_list.json index.html privacy-policy.html sitemap.xml robots.txt package.json package-lock.json"; \
	RESERVED_DIRS="zh ja de fr es pt ar css js images config docs scripts seo .git __pycache__ node_modules"; \
	error=0; \
	for item in $(PROJ_ROOT)/*; do \
	  name=$$(basename "$$item"); \
	  if [ -d "$$item" ]; then \
	    found=0; \
	    for ad in $$RESERVED_DIRS; do [ "$$name" = "$$ad" ] && found=1; done; \
	    if [ "$$found" -eq 0 ]; then \
	      : # tool directory — allowed by default \
	    fi; \
	  elif [ -f "$$item" ]; then \
	    found=0; \
	    for af in $$ALLOWED_FILES; do [ "$$name" = "$$af" ] && found=1; done; \
	    if [ "$$found" -eq 0 ]; then \
	      case "$$name" in \
	        *.py) echo "  ✗ Python script at root: $$name (should be in scripts/)"; error=1 ;; \
	        *.sh) echo "  ✗ Shell script at root: $$name (should be in scripts/)"; error=1 ;; \
	        *.md) echo "  ✗ Loose .md file at root: $$name (should be in docs/)"; error=1 ;; \
	        *)    echo "  ✗ Unexpected file at root: $$name"; error=1 ;; \
	      esac; \
	    fi; \
	  fi; \
	done; \
	if [ "$$error" -eq 0 ]; then \
	  echo "  ✓ All root entries are allowed"; \
	else \
	  echo "FAIL: Unexpected files/dirs in root"; \
	  exit 1; \
	fi

# ==============================================================================
# status — quick project status
# ==============================================================================
.PHONY: status
status:
	@echo "── Git log (last 3) ──"
	@cd "$(PROJ_ROOT)" && git log --oneline -3 2>/dev/null || echo "  (no git history)"
	@echo ""
	@echo "── Uncommitted files ──"
	@cd "$(PROJ_ROOT)" && git status --short 2>/dev/null || echo "  (clean)"
	@echo ""
	@echo "── Feature list status ──"
	@fl="$(PROJ_ROOT)/feature_list.json"; \
	if [ -f "$$fl" ]; then \
	  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); items=d if isinstance(d,list) else d.get('features',d.get('items',[])); c=sum(1 for i in items if i.get('status','').lower() in ('complete','done','finished')); p=sum(1 for i in items if i.get('status','').lower() in ('partial','in-progress','wip','progress')); q=sum(1 for i in items if i.get('status','').lower() in ('planned','todo','backlog')); print(f'  complete: {c}  |  partial: {p}  |  planned: {q}  (total: {len(items)})')" "$$fl"; \
	else \
	  echo "  feature_list.json not found"; \
	fi
	@echo ""
	@echo "── Make targets available ──"
	@echo "  make verify   — project integrity check"
	@echo "  make lint     — code quality check"
	@echo "  make status   — quick project status"
