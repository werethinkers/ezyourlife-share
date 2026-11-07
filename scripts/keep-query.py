"""Make every share page pass its ?query (the person's name: ?to=Rahul&hn=1) on to the live card.

Pages are written by the site's ip-checkout function. Older copies of it forward to a fixed address,
which drops the name, so each person would see a card without their name. This rewrites the forward
to add location.search, and keeps the no-JavaScript refresh only as a fallback inside <noscript>.
Safe to run again: pages already fixed are left as they are.
"""
import base64, pathlib, re, sys

# A 1x1 transparent GIF next to each page. The site loads it as an image (which works across sites, unlike a
# fetch) to know the page is online before anyone sends the link, so WhatsApp always finds the preview.
READY = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")

changed = 0
for f in pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "p").glob("*/**/index.html"):
    s = f.read_text(encoding="utf-8")
    t = re.sub(r'location\.replace\("([^"]+)"\)(?!\s*\+)', r'location.replace("\1" + location.search)', s)
    t = re.sub(r'(?<!<noscript>)(<meta http-equiv="refresh"[^>]*>)', r'<noscript>\1</noscript>', t)
    if t != s:
        f.write_text(t, encoding="utf-8"); changed += 1; print("fixed", f)
    ready = f.parent / "ready.gif"
    if not ready.exists():
        ready.write_bytes(READY); changed += 1; print("ready", ready)
print(f"{changed} page(s) changed")
