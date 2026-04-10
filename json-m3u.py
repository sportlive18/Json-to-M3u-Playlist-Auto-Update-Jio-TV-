#!/usr/bin/env python3
"""
Quick JSON to M3U Converter - Simple Version
Just download and convert - no frills!
"""

import json
import requests

def convert_json_to_m3u():
    # Fetch JSON
    print("Fetching channels...")
    url = "https://raw.githubusercontent.com/dilzyking/Allrounder/refs/heads/main/api/jiotv2.json"
    
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        channels = response.json()
        
        # Create M3U
        m3u = "#EXTM3U\n"
        for ch in channels:
            m3u += f'#EXTINF:-1 tvg-id="{ch.get("channel_id", "")}" tvg-name="{ch.get("channel_name", "Unknown")}" tvg-logo="{ch.get("channel_logo", "")}" group-title="{ch.get("channel_genre", "")}",{ch.get("channel_name", "Unknown")}\n'
            m3u += ch.get('channel_url', '') + "\n"
        
        # Save
        with open('Sportlink.m3u', 'w', encoding='utf-8') as f:
            f.write(m3u)
        
        print(f"Created Sportlink.m3u with {len(channels)} channels!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    convert_json_to_m3u()