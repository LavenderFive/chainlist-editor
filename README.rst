================
chainlist-editor


    A small set of scripts that can alter the state of the cosmostation chainlist!


Pre-reqs
====

1. Your validator is set up in the [validator-registry](https://github.com/eco-stake/validator-registry/tree/master). 
Your `VALIDATOR_REGISTRY_NAME` in `.env` is the folder name you used. 
2. You must have first downloaded Mintscan's [chain-list](https://github.com/cosmostation/chainlist).

Instructions
====

1. poetry init
2. Rename .env.sample to .env
3. run scripts:

```py
python3 src/logo-add.py
```
