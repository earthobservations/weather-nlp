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
$(eval black        := $(venvpath)/bin/black)
$(eval isort        := $(venvpath)/bin/isort)


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
	$(python) -m spacy download en_core_web_md
	$(python) -m spacy download de_core_news_md
	$(python) -m spacy download zh_core_web_md
	wget https://argosopentech.nyc3.digitaloceanspaces.com/argospm/translate-hi_en-1.1.argosmodel --directory-prefix=./var --no-clobber

# Setup Flair
setup-flair: setup-virtualenv
	@# brew install rustup
	@# rustup-init
	@# rustup override set nightly
	$(pip) install flair

# Run tests
test:
	$(pytest) -vvv

# Format code
format:
	isort .
	black .
