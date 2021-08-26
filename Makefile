# ============
# Main targets
# ============


# -------------
# Configuration
# -------------

$(eval venvpath     := .venv)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval spacy        := $(venvpath)/bin/spacy)
$(eval pytest       := $(venvpath)/bin/pytest)


# -----
# Setup
# -----

# Setup Python virtualenv
setup-virtualenv:
	@test -e $(python) || python3 -m venv --system-site-packages $(venvpath)
	@# $(pip) install --editable=.

# Setup prerequisites
setup: setup-virtualenv
	$(pip) install --requirement=requirements.txt
	$(spacy) download en
	$(spacy) download de

# Setup Flair
setup-flair: setup-virtualenv
	@# brew install rustup
	@# rustup-init
	@# rustup override set nightly
	$(pip) install flair

# Run tests
test:
	$(pytest) -vvv
