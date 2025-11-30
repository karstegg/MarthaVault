#!/usr/bin/env python3
"""
Transcribe WhatsApp voice notes with automatic correction of mining site names.
Part of Claude Code skills for MarthaVault.
"""

import sys
import json
import argparse
import os
from datetime import datetime
from pathlib import Path

# Common mining site mis-transcriptions - add more as discovered
CORRECTIONS_DICT = {
    'trinity': 'Nchwaning 3',
    'n3': 'Nchwaning 3',
    'nch3': 'Nchwaning 3',
    'hutt': 'Haut',
    'ubuntu': 'Update',
    'n2': 'Nchwaning 2',
    'nch2': 'Nchwaning 2',
    'gloria': 'Gloria',
    'glory': 'Gloria',
}

def correct_transcription(text: str) -> tuple[str, list[str]]:
    """
    Apply corrections to transcribed text.
    Returns: (corrected_text, list_of_corrections_applied)
    """
    corrected = text
    corrections_applied = []

    for mis_transcribed, correct_term in CORRECTIONS_DICT.items():
        # Case-insensitive search and replace
        pattern_lower = mis_transcribed.lower()
        if pattern_lower in corrected.lower():
            # Find and replace preserving case where possible
            original = corrected
            # Simple case-insensitive replacement
            import re
            pattern = re.compile(re.escape(mis_transcribed), re.IGNORECASE)
            corrected = pattern.sub(correct_term, corrected)

            if original != corrected:
                corrections_applied.append(f"{mis_transcribed} → {correct_term}")

    return corrected, corrections_applied


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe WhatsApp voice notes with mining site corrections'
    )
    parser.add_argument(
        '--contact',
        default='27833911315',
        help='WhatsApp contact phone number (format: 27XXXXXXXXX)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Maximum number of voice notes to process'
    )
    parser.add_argument(
        '--show-corrections',
        action='store_true',
        help='Display all available corrections'
    )

    args = parser.parse_args()

    # If user just wants to see corrections dictionary
    if args.show_corrections:
        print("Available Corrections Dictionary:")
        print("=" * 60)
        for mis, correct in sorted(CORRECTIONS_DICT.items()):
            print(f"  {mis:20} → {correct}")
        print("=" * 60)
        return 0

    print(f"Voice Note Transcription Skill")
    print(f"Contact: {args.contact}")
    print(f"Limit: {args.limit} notes")
    print()
    print("Status: This skill requires manual execution via Claude Code.")
    print("Use: /transcribe-voice-notes to process voice notes")
    print()
    print("Corrections Dictionary Loaded:")
    print(f"  - {len(CORRECTIONS_DICT)} common mining site corrections")

    return 0


if __name__ == '__main__':
    sys.exit(main())
