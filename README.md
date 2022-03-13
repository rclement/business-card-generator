![Banner QR Card](https://business-card-generator.vercel.app/api/card?name=John%20Doe&format=png)

# Business Card Generator

[![CI/CD](https://github.com/rclement/business-card-generator/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/rclement/business-card-generator/actions/workflows/ci-cd.yml)
[![Coverage Status](https://img.shields.io/codecov/c/github/rclement/business-card-generator)](https://codecov.io/gh/rclement/business-card-generator)
[![License](https://img.shields.io/github/license/rclement/business-card-generator)](https://github.com/rmnclmnt/business-card-generator/blob/master/LICENSE)

Everyone needs a business card. Or multiple ones. Or in multiple formats.
Might as well be able to generate them on the fly.

This software allows to generate digital QR-code business cards:

- [MeCard](https://en.wikipedia.org/wiki/MeCard_(QR_code))
- [vCard](https://en.wikipedia.org/wiki/VCard)

## Deployment

If you do not trust the official deployment, feel free to deploy your own!

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https://github.com/rclement/business-card-generator)
[![Deploy with Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/rclement/business-card-generator)

## Development

### Python

```bash
cp .example.env .env
pipenv install -d
pipenv shell
inv qa
flask run
```

### VSCode

If using VSCode, use the following configuration in `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "business_card_generator.app:create_app",
        "FLASK_ENV": "development"
      },
      "args": ["run", "--no-debugger"],
      "jinja": true,
      "envFile": "",
      "justMyCode": false
    },
    {
      "name": "tests",
      "type": "python",
      "request": "test",
      "justMyCode": false
    }
  ]
}
```

## Inspiration

- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats)
- [François Best Business Card](https://francoisbest.com/business-card)

## License

Licensed under GNU Affero General Public License v3.0 (AGPLv3)

Copyright (c) 2022 - present  Romain Clement
