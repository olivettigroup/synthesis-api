# The Synthesis Project - Public API / Web Interface
[![Circle CI](https://circleci.com/gh/olivettigroup/synthesis-api.svg?style=svg&circle-token=224606a43088c3248ea1363602b326f8194c9d37)](https://circleci.com/gh/olivettigroup/synthesis-api)

Public-facing API that interfaces with the Synthesis Project database.

**API LINK** https://synthesis-api.herokuapp.com/materials

(Supports anonymous GET requests)

## Dependencies

**HOW TO USE**

To use the API, all you need is something that can interface with a REST API (read: pretty much everything). Some examples might be the `requests` library for Python or using the ajax methods in JQuery.

**(If you want to deploy your own version of this API)**

Install all the stuff in `requirements.txt`. You shouldn't need anything else besides that to spin up your own instance of this API.

## Overview of Usage

This repository defines a **REST API** built using the `Eve` library for Python. The goal of the API is to expose some synthesis data for various materials, compiled automatically from literature text-mining. Some example routes are given as follows:

- (see everything) https://synthesis-api.herokuapp.com/materials
- (see one material) https://synthesis-api.herokuapp.com/materials/LiCoO2 
