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
    # Using the raw URL to avoid HTML content
    url = "https://raw.githubusercontent.com/Anasvirat18/Jio_/main/stream.json"
    
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        
        # Check if response is actually JSON
        try:
            data = response.json()
        except ValueError:
            print("Error: Response is not valid JSON. Check the source URL.")
            return

        # Handle both list and dictionary structures
        channels_list = []
        if isinstance(data, list):
            channels_list = data
        elif isinstance(data, dict):
            # If it's a dictionary of channel objects, iterate through its values
            for cid, details in data.items():
                if isinstance(details, dict):
                    # Inject ID if not present
                    if "channel_id" not in details:
                        details["channel_id"] = cid
                    channels_list.append(details)
        
        # Create M3U
        m3u = "#EXTM3U\n"
        for ch in channels_list:
            # Extract name from URL if channel_name is missing
            name = ch.get("channel_name")
            if not name:
                # Try to get it from the URL (e.g., .../CNBC_Tv18_Prime_HD_MOB/...)
                stream_url = ch.get("url", ch.get("channel_url", ""))
                if "bpk-tv/" in stream_url:
                    name = stream_url.split("bpk-tv/")[1].split("/")[0].replace("_", " ")
                else:
                    name = f"Channel {ch.get('channel_id', 'Unknown')}"
            
            logo = ch.get("channel_logo", "")
            genre = ch.get("channel_genre", "General")
            
            m3u += f'#EXTINF:-1 tvg-id="{ch.get("channel_id", "")}" tvg-name="{name}" tvg-logo="{logo}" group-title="{genre}",{name}\n'
            
            # DRM Keys - Handle different possible field names
            key_id = ch.get("keyId", ch.get("kid"))
            key = ch.get("key")
            
            # If key is a script URL instead of a hex key, we might need special handling
            # For now, we'll just include it if it exists
            if key_id and key:
                m3u += '#KODIPROP:inputstream.adaptive.license_type=clearkey\n'
                m3u += f'#KODIPROP:inputstream.adaptive.license_key={key_id}:{key}\n'
                
            ch_url = ch.get('channel_url', ch.get('url', ''))
            m3u += ch_url + "\n\n"
        
        # Save
        output_file = 'jtv.m3u'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(m3u)
        
        print(f"Created {output_file} with {len(channels_list)} channels!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    convert_json_to_m3u()
