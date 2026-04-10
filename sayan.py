#!/usr/bin/env python3
"""
Generator Script - Generate M3U playlist
"""

import json
import requests

def generate_m3u():
    url = "https://allinonereborn.online/jstrweb2/jstr.json"
    print(f"[*] Fetching channels from API: {url}...")
    
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        channels = response.json()
        print(f"[+] Successfully fetched {len(channels)} channels.")
        
        m3u_file = "sayan.m3u"
        with open(m3u_file, "w", encoding="utf-8") as f:
            f.write('#EXTM3U x-tvg-url="https://raw.githubusercontent.com/mitthu786/tvepg/main/tataplay/epg.xml.gz"\n\n')
            
            for ch in channels:
                channel_id = ch.get("channel_id", "")
                name = ch.get("name", "Unknown Channel")
                logo = ch.get("logo", "")
                category = ch.get("category", "")
                mpd = ch.get("mpd", "")
                referer = ch.get("referer", "")
                user_agent = ch.get("userAgent", "")
                drm = ch.get("drm", {})
                
                # Skip invalid or placeholder channels
                if not mpd or mpd.strip() == "":
                    continue
                    
                # Write EXTINF
                f.write(f'#EXTINF:-1 tvg-id="{channel_id}" tvg-logo="{logo}" group-title="{category}",{name}\n')
                
                # Check for DRM properties
                if drm and isinstance(drm, dict):
                    for k, v in drm.items():
                        if k != "null" and v != "null" and k and v:
                            f.write('#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
                            f.write(f'#KODIPROP:inputstream.adaptive.license_key={k}:{v}\n')
                            break # Assume only one key pair is needed
                
                # Construct stream URL with HTTP headers (Kodi style)
                stream_url = mpd
                headers = []
                if user_agent and user_agent != "null":
                    headers.append(f"User-Agent={user_agent}")
                if referer and referer != "null":
                    headers.append(f"Referer={referer}")
                    
                if headers:
                    stream_url += "|" + "&".join(headers)
                    
                f.write(f"{stream_url}\n\n")
                
        print(f"[*] Playlist generated successfully and saved to {m3u_file}")
        
    except Exception as e:
        print(f"[-] Error: {e}")
        # Optionally exit with 1 to fail the workflow if the fetch fails
        # exit(1) 

if __name__ == "__main__":
    generate_m3u()