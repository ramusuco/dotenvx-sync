# dxsync

CLI tool for syncing encrypted `.env` files across teams using dotenvx.

## Features

- **Simple CLI** - `dxsync init`, `dxsync encrypt`, `dxsync decrypt`
- **Per-environment encryption** - Separate keys for dev, stg, prd
- **Non-destructive** - Never overwrites your local plaintext `.env` files
- **Configurable** - Customize paths via `dxsync.json`

## Prerequisites

- Python 3.11+
- [dotenvx](https://dotenvx.com/docs/install) - Install via your preferred method:

```bash
# npm
npm install -g @dotenvx/dotenvx

# brew
brew install dotenvx/brew/dotenvx

# curl
curl -sfS https://dotenvx.sh | sh
```

## Installation

```bash
pip install dxsync
```

## Quick Start

```bash
# 1. Initialize in your project
cd your-project
dxsync init

# 2. Create your plaintext env file
echo "API_KEY=secret123" > .env/dev

# 3. Encrypt it
dxsync encrypt dev
# → Creates enc/.env.dev.enc and .env/keys/dev.keys

# 4. Share .env/keys/dev.keys with your team securely

# 5. Commit the encrypted file
git add enc/.env.dev.enc
git commit -m "Add encrypted dev env"
```

## Directory Structure

After `dxsync init`:

```
your-project/
├── dxsync.json             # Configuration
├── enc/                    # Encrypted files (commit these)
│   └── .env.dev.enc
├── .env/                   # Local files (gitignored)
│   ├── dev                 # Plaintext source
│   ├── keys/               # Key files
│   │   └── dev.keys
│   └── latest/             # Decrypted output
│       └── .env.dev
└── .gitignore              # Updated by dxsync init
```

## Usage

### Encrypt

Add or update keys in your plaintext file, then encrypt:

```bash
# Edit .env/dev with your values
dxsync encrypt dev
```

- First run: auto-generates key file and `.enc`
- Subsequent runs: adds new keys to existing `.enc`

### Decrypt

Get the key file from your team, then:

```bash
dxsync decrypt dev
# → Output: .env/latest/.env.dev
```

### Change existing values

1. Remove the key from `enc/.env.dev.enc`
2. Update value in `.env/dev`
3. Run `dxsync encrypt dev`

## Configuration

Edit `dxsync.json` to customize:

```json
{
  "envs": ["dev", "stg", "prd"],
  "env_dir": ".env",
  "enc_dir": "enc",
  "work_dir": "tmp/dxsync"
}
```

Or use `pyproject.toml`:

```toml
[tool.dxsync]
envs = ["dev", "stg", "prd"]
env_dir = ".env"
enc_dir = "enc"
```

## Design Principles

- **Append-only** - Existing keys in `.enc` are never auto-overwritten
- **Non-destructive** - Decryption outputs to `latest/`, not your working `.env`
- **Explicit reset** - Delete `.enc` manually to regenerate

## License

MIT

## References

- [dotenvx Documentation](https://dotenvx.com/docs)
