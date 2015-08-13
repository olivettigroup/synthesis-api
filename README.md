# The Synthesis Project - Public API / Web Interface
[![Circle CI](https://circleci.com/gh/olivettigroup/synthesis-api.svg?style=svg&circle-token=224606a43088c3248ea1363602b326f8194c9d37)](https://circleci.com/gh/olivettigroup/synthesis-api)

Public-facing API that interfaces with the Synthesis Project database

## Dependencies

Install all the stuff in `requirements.txt`. You shouldn't need anything else besides that to spin up your own instance of this API.

To use the API, all you need is something that can interface with a REST API (read: pretty much everything). Some examples might be the `requests` library for Python or using the ajax methods in JQuery.

## Documentation

__Read the documentation at `docs/html/index.html`.__ 

You can rebuild the documentation by running 
    
    sphinx-build . html 

from the `docs` directory at any time. If you want to regenerate the `.rst` files, run 

    sphinx-apidoc -ef -o docs synthesisapi

from the repo root. You'll want to rebuild the documentation if you've regenerated these files.


