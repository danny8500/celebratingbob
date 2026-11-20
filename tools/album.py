"""Refresh album.json from the public Google Photos share link."""
import json, re, urllib.request
URL = "https://photos.app.goo.gl/8h5mQQfjuheReAA48"
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=60).read().decode("utf8", "replace")
seen, photos = set(), []
for u, w, h in re.findall(r'\["(https://lh3\.googleusercontent\.com/pw/[^"]+)",(\d+),(\d+)', html):
    if u in seen: continue
    seen.add(u); photos.append({"u": u, "w": int(w), "h": int(h)})
if not photos: raise SystemExit("no photos found; leaving album.json unchanged")
json.dump({"album": URL, "photos": photos}, open("album.json", "w"), separators=(",", ":"))
print(len(photos), "photos")
