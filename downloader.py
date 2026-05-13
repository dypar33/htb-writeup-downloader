import requests
import os
import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bulk download HackTheBox official writeup PDFs"
    )
    parser.add_argument(
        "-t", "--token",
        required=True,
        metavar="TOKEN",
        help="HTB App Token (omit the 'Bearer ' prefix)"
    )
    parser.add_argument(
        "-m", "--machines",
        default="machines.txt",
        metavar="FILE",
        help="Path to machine-name list file, one name per line (default: machines.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        default="writeups",
        metavar="DIR",
        help="Output directory for downloaded PDFs (default: writeups)"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=2.0,
        metavar="SECONDS",
        help="Delay between requests in seconds (default: 2.0)"
    )
    return parser.parse_args()


def load_machines(path):
    """Read machine names from a file, skipping blank lines and comments."""
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def download_writeups(token, machines, output_dir, delay):
    headers = {
        "Host": "labs.hackthebox.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {token}",
        "Origin": "https://app.hackthebox.com",
        "Referer": "https://app.hackthebox.com/",
    }

    os.makedirs(output_dir, exist_ok=True)

    for name in machines:
        # Step 1: Resolve machine name to numeric ID
        profile_resp = requests.get(
            f"https://labs.hackthebox.com/api/v4/machine/profile/{name}",
            headers=headers,
        )

        if profile_resp.status_code != 200:
            print(f"[!] {name}: profile lookup failed ({profile_resp.status_code})")
            continue

        machine_id = profile_resp.json()["info"]["id"]
        print(f"[*] {name} -> ID: {machine_id}")

        # Step 2: Download the official writeup PDF
        pdf_resp = requests.get(
            f"https://labs.hackthebox.com/api/v4/machine/writeup/{machine_id}",
            headers=headers,
        )

        if pdf_resp.status_code == 200:
            path = os.path.join(output_dir, f"{name}.pdf")
            with open(path, "wb") as f:
                f.write(pdf_resp.content)
            print(f"[+] Saved {name}.pdf")
        else:
            print(f"[-] {name}: no writeup available (status {pdf_resp.status_code})")

        time.sleep(delay)


if __name__ == "__main__":
    args = parse_args()

    try:
        machines = load_machines(args.machines)
    except FileNotFoundError:
        print(f"[!] Machine list not found: {args.machines}")
        raise SystemExit(1)

    if not machines:
        print(f"[!] No machine names found in {args.machines}")
        raise SystemExit(1)

    print(f"[*] Loaded {len(machines)} machine(s) from {args.machines}")
    download_writeups(args.token, machines, args.output, args.delay)
