# The Synthesis Project - Public API / Web Interface
[![Circle CI](https://circleci.com/gh/olivettigroup/synthesis-api.svg?style=svg&circle-token=224606a43088c3248ea1363602b326f8194c9d37)](https://circleci.com/gh/olivettigroup/synthesis-api)

Public-facing API that interfaces with the Synthesis Project database

## Dependencies

Install all the stuff in `requirements.txt`. You shouldn't need anything else besides that to spin up your own instance of this API.

To use the API, all you need is something that can interface with a REST API (read: pretty much everything). Some examples might be the `requests` library for Python or using the ajax methods in JQuery.

## Overview of Usage (Not fully implemented yet!)

This repository defines a **REST API** built using the `Eve` library for Python. The goal of the API is to expose some synthesis data for various materials, compiled automatically from literature text-mining. Some example routes are given as follows:

### Getting high-level info about a material

**`GET /api/[material identifier]/`**
    
    RETURNS:
    {
        'success': (int) true/false,
        'dois': (list of strings) [ a sample (truncated) list of article DOIs which discuss synthesizing this material ],
        'num_papers': (int) number of papers in our database which match this query
    }

Here, the `[material identifier]` can be a chemical formula (e.g. `TiO2`) or an MPID (as defined in the [**Materials Project**](http://materialsproject.org)). Note that the returned data may correspond to a broader category of material than specified in the `[material identifier]` in the case of using MPIDs. If `success` is `false`, then all other fields will be `null`.

### Getting sample synthesis paragraphs about a material

**`GET /api/[material identifier]/paragraphs/`**
    
    RETURNS:
    {
        'success': (int) true/false,
        'paragraphs': (list of strings) [ a sample (truncated) list of plaintext synthesis paragraphs for this material ],
        'dois': (list of strings) [ article DOIs, where each DOI corresponds to the source of the paragraph with matching list index ]
    }

Here, the `[material identifier]` can be a chemical formula (e.g. `TiO2`) or an MPID (as defined in the [**Materials Project**](http://materialsproject.org)). Note that the returned data may correspond to a broader category of material than specified in the `[material identifier]` in the case of using MPIDs. If `success` is `false`, then all other fields will be `null`.

### Getting aggregated synthesis parameters about a material

**`GET /api/[material identifier]/synthesis/`**
    
    RETURNS:
    {
        'success': (int) true/false,
        'temp_hist_x': (list of floats) [ x-values (degrees C) for a normalized temperature usage histogram ],
        'temp_hist_y': (list of floats) [ y-values (arb. units) for a normalized temperature usage histogram ],
        'common_precursors': (list of strings) [ list of top-used precursors, solvents, etc. ]
        'dois': (list) [ article DOIs, where each DOI corresponds to the source of the paragraph with matching list index ]
    }

Here, the `[material identifier]` can be a chemical formula (e.g. `TiO2`) or an MPID (as defined in the [**Materials Project**](http://materialsproject.org)). Note that the returned data may correspond to a broader category of material than specified in the `[material identifier]` in the case of using MPIDs. If `success` is `false`, then all other fields will be `null`.

## Documentation

__Read the documentation at `docs/html/index.html`.__ 

You can rebuild the documentation by running 
    
    sphinx-build . html 

from the `docs` directory at any time. If you want to regenerate the `.rst` files, run 

    sphinx-apidoc -ef -o docs synthesisapi

from the repo root. You'll want to rebuild the documentation if you've regenerated these files.


