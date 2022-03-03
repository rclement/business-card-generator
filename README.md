# Business Card Generator

Everyone needs a business card. Or multiple ones. Or in multiple formats.
Might as well be able to generate them on the fly.

This software allows to generate digital QR-code business cards:

- [MeCard](https://en.wikipedia.org/wiki/MeCard_(QR_code))
- [vCard](https://en.wikipedia.org/wiki/VCard)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https://github.com/rclement/business-card-generator)

## Development

### Python

```bash
cp .example.env .env
pipenv install -d
pipenv shell
inv qa
```

### VSCode

If using VSCode, use the following configuration in `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["--port=8000", "--factory", "business_card_generator.app:create_app"],
      "envFile": "",
      "jinja": true,
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
