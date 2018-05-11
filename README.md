# opeb-submission-api

- [Summary](#summary)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Spec](#spec)
  - [API](#api)

## Summary

## Requirements
```
  pip3 install pipenv
  pipenv install -r requirements.txt
  yarn global add check_api
```

## Usage
### Spec
Generate and validate the API spec against [OpenAPIv3](https://www.openapis.org/)
```
pipenv run './api.py spec'
```
### API
Server the API
```
pipenv run './api.py api'
```