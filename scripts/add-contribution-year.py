"""Add a persistent first-contribution row to generated GitHub stats cards."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

for path in sorted(Path('profile').glob('stats-*.svg')):
    svg = path.read_text()
    if 'id="first-contribution"' in svg:
        continue
    root = ET.fromstring(svg)
    height = int(root.attrib['height'])
    body = root.find('.//{http://www.w3.org/2000/svg}g[@data-testid="main-card-body"]')
    rows = body.find('{http://www.w3.org/2000/svg}svg').findall('{http://www.w3.org/2000/svg}g')
    row_y = len(rows) * 25
    # Extend the card by one row while preserving the generator's formatting.
    svg = re.sub(r'height="\d+"', f'height="{height + 25}"', svg, count=1)
    viewbox = root.attrib['viewBox'].split()
    viewbox[3] = str(height + 25)
    svg = re.sub(r'viewBox="[^"]+"', f'viewBox="{" ".join(viewbox)}"', svg, count=1)
    svg = svg.replace('</desc>', ', First GitHub contribution: 2016</desc>', 1)
    row = f'''
      <g id="first-contribution" transform="translate(0, {row_y})">
        <g class="stagger" style="animation-delay: 1200ms" transform="translate(25, 0)">
          <svg class="icon" viewBox="0 0 16 16" width="16" height="16">
            <path d="M4 0h1.5v2h5V0H12v2h1.25A1.75 1.75 0 0 1 15 3.75v10.5A1.75 1.75 0 0 1 13.25 16H2.75A1.75 1.75 0 0 1 1 14.25V3.75A1.75 1.75 0 0 1 2.75 2H4V0ZM2.5 6v8.25c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25V6h-11Z" />
          </svg>
          <text class="stat bold" x="25" y="12.5">First GitHub contribution:</text>
          <text class="stat bold" x="224.01" y="12.5" data-testid="first-contribution">2016</text>
        </g>
      </g>
'''
    marker = '\n    </svg>'
    assert marker in svg, f'Unexpected stats card structure: {path}'
    before, after = svg.rsplit(marker, 1)
    svg = before + row + marker + after
    ET.fromstring(svg)
    path.write_text(svg)
