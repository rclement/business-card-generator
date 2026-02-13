# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Use Python 3.14
- Update dependencies

### Internal
- Add `uv` lockfile maintenance GitHub Workflow

## [0.5.1] - 2025-11-06
### Fixed
- Typo for cellphone field display
- Display errors and field values with GET to home form

## [0.5.0] - 2025-11-06
### Added
- Proper form fields data validation
- Cellphone field (only available for vCard format) (thanks @zerabba)

### Changed
- Use Python 3.13.9
- Update dependencies
- Modernize Python type hints

## [0.4.0] - 2025-09-29
### Fixed
- Code coverage reporting without using Codecov service

### Changed
- Use Python 3.13.5
- Update dependencies
- Replace usage of `safety` with `pip-audit`
- Migrate to `pydantic` version 2
- Use `uv` package manager instead of `pipenv`
- Use `ruff` instead of `black` and `flake8`

## [0.3.0] - 2023-08-03
### Fixed
- Generate QR codes with Unicode (UTF-8) encoding

### Changed
- Vendor external CSS stylesheet
- Use Python 3.11.4
- Update dependencies

## [0.2.0] - 2022-08-30
### Changed
- Use Python 3.10.6
- Update dependencies

## [0.1.0] - 2022-03-20
### Added
- Initial release of `business-card-generator`
- Support for QR-Code vCard and MeCard
- Export format support for VCF, SVG, PNG

[Unreleased]: https://github.com/rclement/business-card-generator/compare/0.5.1...HEAD
[0.5.1]: https://github.com/rclement/business-card-generator/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/rclement/business-card-generator/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/rclement/business-card-generator/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/rclement/business-card-generator/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/rclement/business-card-generator/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/rclement/business-card-generator/releases/tag/0.1.0
