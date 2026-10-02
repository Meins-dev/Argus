# ARGUS

Local Gemini Live desktop assistant with a PyQt6 interface, voice interaction, detachable panels, and optional browser, file, screen, and messaging tools.

ARGUS also includes a dedicated presentation studio that creates, edits,
redesigns, and extends editable widescreen `.pptx` decks from documents, data,
images, audio, and video, with optional PDF export. See the
[usage guide](docs/USAGE.md#6-powerpoint-presentations) for examples.

## Requirements

You need **Python 3.11 or newer** installed to set up and run ARGUS. Confirm
your Python version before continuing:

```bash
python --version
```

## Releases

Versioning starts at **0.1.0**. The desktop build workflow produces a Windows
installer, a macOS disk image, and a Linux Debian package when a `v*` tag is
pushed. It attaches SHA-256 checksums to the GitHub release. The
[release workflow](.github/workflows/release.yml) is configured, but no binary
release is published yet: the canonical public repository still needs its
Argus URL selected, then `v0.1.0` must be pushed there. Source installation
remains available after cloning the canonical repository.

## Quick start (Windows, macOS, Linux)

In Terminal, run:

```bash
git clone <canonical Argus repository URL> Argus
cd Argus
python scripts/setup_argus.py
```

On Windows, you can double-click `scripts/setup_argus.bat` instead.

Open `.env`, add your `GEMINI_API_KEY`, then launch ARGUS:

```bash
argus
```

You only need to run setup once. Activate `.venv` when opening a new terminal,
then type `argus`.

ARGUS's core UI, Gemini connection, presentations, research, files, and CLI are
cross-platform. Some computer-control, email, media, and browser integrations
depend on permissions and available applications on each operating system.

## Hosted web application

The repository also contains a multi-user FastAPI service and a Next.js web
client. Hosted sessions use Postgres for user-scoped memory and configuration,
Redis for request quotas, encrypted per-user Gemini keys, and Gemini Live over
an authenticated WebSocket. The desktop launcher continues to use its local
stores and full local action inventory.

Start the complete local web stack with Docker:

```bash
docker compose up --build
```

Then open `http://localhost:3000`. To run each service directly:

```bash
# API
cp .env.example .env
alembic upgrade head
uvicorn api.server:app --reload

# Web client
cd web
cp .env.example .env.local
npm install
npm run dev
```

Production templates are included for Fly.io (`fly.toml`), Render
(`render.yaml`), and Vercel (`web/vercel.json`). Configure `DATABASE_URL`,
`REDIS_URL`, `JWT_SECRET`, `ARGUS_ENCRYPTION_KEY`, and `CORS_ORIGINS` on the
API host. Set `NEXT_PUBLIC_API_BASE_URL` to the API's public base URL in the
web deployment; the client derives both HTTP and WebSocket URLs from it. Set
`CORS_ORIGINS` to the deployed web origin. The deployment workflow runs
manually after the Fly and Vercel repository secrets have been added.

## Manual setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cp .env.example .env
./scripts/install_argus_cli.sh
argus
```

Set `GEMINI_API_KEY` in `.env` before launch. Optional settings such as voice and local API keys are documented in `.env.example`.

### Launch with `argus`

The CLI launcher is included in this repository. After cloning and completing
the one-time setup, install it for your user with:

```bash
./scripts/install_argus_cli.sh
```

Open a new terminal (or reload your shell profile), then start ARGUS with:

```bash
argus
```

Before packaging or releasing the desktop app, run the side-effect-safe
capability audit:

```bash
argus --self-test
```

The audit exercises voice/tool contracts, messaging routing and approval
boundaries, a local browser interaction, isolated file operations, vision,
agent recovery, and memory. It never sends a real message or performs a live
desktop mutation. Results that still require a person, account, or physical
device are labeled `LIVE CHECK REQUIRED`, and a JSON report is written under
`.qa-artifacts/`.

Alternatively, from an activated virtual environment, `python3 -m pip install -e .`
installs the same `argus` command through the standard Python package entry point.

## Documentation

- [Changelog](CHANGELOG.md)
- [Usage guide](docs/USAGE.md)
- [Tutorial](docs/TUTORIAL.md)
- [Complete QA and bug-audit guide](docs/QA.md)
- [Contribution notes](CONTRIBUTING.md)

## Availability

- **Release:** v0.1.0 packaging and publish steps are configured in the
  [release workflow](.github/workflows/release.yml). Installers and checksums
  will exist only after the canonical Argus repository URL is selected, the tag
  is pushed, and CI succeeds.
- **Desktop requirements:** the [measurement report](docs/benchmarks/desktop.md)
  links to the [raw samples](docs/benchmarks/desktop-0.1.0-20261002T234124Z.csv).
  It contains a real 60-second idle result; typical/intense scenarios and
  official minimum/recommended hardware remain undetermined.
- **Web capacity:** the [load report](docs/benchmarks/web.md) links to the
  [raw stage summary](docs/benchmarks/web-0.1.0-native-api-sqlite-20261002T233159Z.json).
  Native SQLite/API HTTP load reached 40 sessions without crossing the test
  threshold; no saturation was observed through 40 and the exact maximum is
  unknown. Docker Compose and PostgreSQL/Redis capacity remain unmeasured.
- **Policies:** [privacy](PRIVACY.md), [terms](TERMS.md) and
  [security](SECURITY.md) are published as code-based models; legal review is
  still required before commercial use.
- **Public URLs:** the canonical repository slug and production website domain
  are not selected here. Configure `PUBLIC_ARGUS_REPOSITORY_URL` and
  `PUBLIC_ARGUS_SITE_URL` in the Astro site's `.env.example` after those
  decisions; the latter supplies the site's canonical/Open Graph base URL.

## Configuration files

Template files are included for local setup:

- `.env.example`
- `config/api_keys.example.json`
- `config/layout_settings.example.json`
- `config/ui_settings.example.json`
- `memory/long_term.example.json`
- `memory/task_history.example.json`

## Publishing checklist

- Keep `.env` and local secret files out of git.
- Do not commit `memory/long_term.json` or `config/api_keys.json`.
- Run `python3 -m py_compile main.py ui.py` before tagging a release.

## License

MIT License, see [LICENSE](LICENSE).
