# htb-writeup-downloader

Bulk-download official HackTheBox writeup PDFs using the HTB API.

## Requirements

```
pip install requests
```

## Setup

1. Get your **App Token** from [HTB Profile → API Token](https://app.hackthebox.com/account-settings).
2. Edit `machines.txt` and list the machine names you want to download (one per line).

## Usage

```
python downloader.py -t <YOUR_APP_TOKEN> [options]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-t`, `--token` | *(required)* | HTB App Token (without the `Bearer ` prefix) |
| `-m`, `--machines` | `machines.txt` | Path to the machine-name list file |
| `-o`, `--output` | `writeups/` | Directory to save downloaded PDFs |
| `-d`, `--delay` | `2.0` | Seconds to wait between requests |

### Examples

```bash
# Basic usage
python downloader.py -t eyJ0eXAi...

# Custom machine list and output folder
python downloader.py -t eyJ0eXAi... -m my_list.txt -o pdfs/

# Faster downloads (reduce delay)
python downloader.py -t eyJ0eXAi... -d 1
```

## machines.txt format

```
# Lines starting with '#' are comments
Lame
Legacy
Devel
Bastard
```

## Notes

- Only **retired** machines have official writeups available.
- Downloaded PDFs are saved to the output directory (`writeups/` by default).
- The `writeups/` directory and all `.pdf` files are excluded from git via `.gitignore`.
