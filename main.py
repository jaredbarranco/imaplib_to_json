from imap import imap_to_json
import os
import sys

# List of required environment variables
required_env_vars = ["IMAP_SERVER", "IMAP_USER", "IMAP_PASS"]

# Check for missing variables
missing_vars = [var for var in required_env_vars if os.getenv(var) is None]

if missing_vars:
    print(
        f"Error: Missing required environment variables: {', '.join(missing_vars)}", file=sys.stderr)
    sys.exit(1)

imap_to_json(os.getenv('IMAP_SERVER'), os.getenv(
    'IMAP_USER'), os.getenv('IMAP_PASS'))
