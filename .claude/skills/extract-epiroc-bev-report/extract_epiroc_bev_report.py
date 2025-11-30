#!/usr/bin/env python3
"""
Extract Epiroc BEV Weekly Report - Extracts key sections from Epiroc BRMO weekly PDF reports
into structured markdown format using Claude Code's native PDF reading capabilities.

This script is invoked via Claude Code slash command and leverages Claude's vision
and text extraction capabilities to read the PDF.
"""

import argparse
import sys
import os
from pathlib import Path
import json


def find_pdf_file(week_num, site="brmo"):
    """Find the Epiroc PDF report in Week N directory"""
    week_dir = Path(f"Week {week_num}")

    if not week_dir.exists():
        print(f"Error: Week {week_num} directory not found", file=sys.stderr)
        return None

    # Look for BRMO weekly report pattern
    pdf_files = list(week_dir.glob("BRMO weekly report*.pdf"))

    if not pdf_files:
        print(f"Error: No BRMO weekly report PDF found in Week {week_num}/", file=sys.stderr)
        return None

    return pdf_files[0]




def main():
    parser = argparse.ArgumentParser(
        description="Extract key sections from Epiroc BEV weekly PDF reports using Claude Code"
    )
    parser.add_argument(
        "week",
        nargs="?",
        type=int,
        help="Week number"
    )
    parser.add_argument(
        "--week",
        type=int,
        dest="week_arg",
        help="Week number (named argument)"
    )
    parser.add_argument(
        "--site",
        type=str,
        default="brmo",
        help="Site name (default: brmo)"
    )

    args = parser.parse_args()

    # Determine week number from positional or named argument
    week_num = args.week or args.week_arg

    if not week_num:
        print("Error: Week number required. Usage: extract_epiroc_bev_report.py --week=16 or 16",
              file=sys.stderr)
        sys.exit(1)

    # Find PDF file
    pdf_path = find_pdf_file(week_num, args.site)
    if not pdf_path:
        sys.exit(1)

    print(f"Found PDF: {pdf_path}", file=sys.stderr)
    print(f"Note: Please run via Claude Code slash command for automatic PDF extraction", file=sys.stderr)

    # Output request info that Claude Code will process
    request_info = {
        "skill": "extract-epiroc-bev-report",
        "week": week_num,
        "pdf_file": str(pdf_path),
        "output_file": f"Week {week_num}/Epiroc_BEV_Weekly_Report_Week{week_num}_Extracted.md"
    }

    # Print as JSON for Claude Code integration
    print(json.dumps(request_info), file=sys.stdout)
    return 0


if __name__ == "__main__":
    main()
