"""Refresh album.json from the public Google Photos share link."""
import json, re, urllib.request
URL = "https://photos.app.goo.gl/8h5mQQfjuheReAA48"
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=60).read().decode("utf8", "replace")
# Each photo entry looks like: ["AF1Qip..",["https://lh3..",w,h,...,[..]],takenMs,"..",tzMs,uploadedMs,...]
PAT = r'\["(https://lh3\.googleusercontent\.com/pw/[^"]+)",(\d+),(\d+),[^"]*?\]\],(-?\d+),"'
seen, photos = set(), []
for u, w, h, t in re.findall(PAT, html):
    if u in seen: continue
    seen.add(u); photos.append({"u": u, "w": int(w), "h": int(h), "t": int(t)})
if not photos: raise SystemExit("no photos found; leaving album.json unchanged")
json.dump({"album": URL, "photos": photos}, open("album.json", "w"), separators=(",", ":"))
print(len(photos), "photos")
