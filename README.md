![Banner QR Card](https://business-card-generator.vercel.app/vcard.svg?firstname=Romain&lastname=Clement&picture=https%3A%2F%2Fromain-clement.net%2Fstatic%2Ficon.png&company=Freelance&job=Software+|+Data+|+AI&email=contact%2Bgithub%40romain-clement.net&phone=&website=https%3A%2F%2Fromain-clement.net)

# Business Card Generator

[![CI/CD](https://github.com/rclement/business-card-generator/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/rclement/business-card-generator/actions/workflows/ci-cd.yml)
[![License](https://img.shields.io/github/license/rclement/business-card-generator)](https://github.com/rmnclmnt/business-card-generator/blob/master/LICENSE)

Everyone needs a business card. Or multiple ones. Or in multiple formats.
Might as well be able to generate them on the fly.

This software allows to generate digital QR-code business cards:

- [MeCard](https://en.wikipedia.org/wiki/MeCard_(QR_code))
- [vCard](https://en.wikipedia.org/wiki/VCard)

## Usage

The easiest way to generate a business card is to use the online
[web application](https://business-card-generator.vercel.app).

You can also integrate URLs for website/keynotes integration using the following scheme:

```
https://business-card-generator.vercel.app/<card-type>.<card-format>?<card-parameters>
```

Available card types:

- `vcard`
- `mecard`

Available card formats:

- `svg`
- `png`
- `vcf`

Available card parameters:

| Parameter   | Format                | Required | Description            |
| ----------- | --------------------- | -------- | ---------------------- |
| `firstname` | `string`              | Yes      | First name             |
| `lastname`  | `str`                 | Yes      | Last name              |
| `nickname`  | `str`                 | No       | Nickname               |
| `birthday`  | `date` (`YYYY-MM-DD`) | No       | Birthday               |
| `company`   | `str`                 | No       | Company name           |
| `job`       | `str`                 | No       | Job title              |
| `email`     | `EmailStr`            | No       | E-mail address         |
| `phone`     | `str`                 | No       | Phone number           |
| `website`   | `HttpUrl`             | No       | Website URL            |
| `picture`   | `HttpUrl`             | No       | Picture URL            |
| `street`    | `str`                 | No       | Street number and name |
| `city`      | `str`                 | No       | City                   |
| `zipcode`   | `str`                 | No       | Zipcode                |
| `state`     | `str`                 | No       | State or region        |
| `country`   | `str`                 | No       | Country                |

## Deployment

If you do not trust the official deployment, feel free to deploy your own!

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https://github.com/rclement/business-card-generator)
[![Deploy with Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/rclement/business-card-generator)

## Development

### Python

```bash
cp .example.env .env
uv sync
uv run inv qa
uv run flask run
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
