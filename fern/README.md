# Fern scaffold (proposal)

This directory is a proposal for generating the Castle Python SDK surface with
[Fern](https://buildwithfern.com) from an OpenAPI specification.

## Layout

- `fern.config.json` — organization name and pinned Fern CLI version.
- `generators.yml` — declares the API spec and the `fern-python-sdk` generator group.
- `openapi/openapi.yml` — OpenAPI spec for the Castle scoring, Lists, Privacy
  and Events endpoints used as the generator input.

## Usage

```bash
npm install -g fern-api
fern check
fern generate --group python-sdk --local
```

Generated code is written to `../generated/python` and is not committed.
