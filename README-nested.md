# Dr. Mallika Kumar — Portfolio Website

Official portfolio of **Dr. Mallika Kumar**, Professor of Economics and Founder Coordinator of the Office of International Programmes (OIP) at Shri Ram College of Commerce (SRCC), University of Delhi.

## Overview

A single-file, fully responsive portfolio website with a built-in admin edit mode. Built with pure HTML5, CSS3 and vanilla JavaScript — no frameworks, no build step.

## Features

- Sticky navigation with smooth scroll
- Hero section with editable profile photo
- About section with four-paragraph biography
- 12 Key Positions & Affiliations
- 18-entry experience timeline (2010–2025)
- 23 publications with filter tabs (Scopus, UGC-Care, Journals, Books)
- 4 Awards & Honours
- Global Reach with interactive SVG world map
- 14 International MoUs in a styled table
- Photo gallery with upload support
- Contact section with form
- Admin edit mode (SHA-256 password auth)
- localStorage persistence
- Export/Reset data controls
- Fully responsive (desktop-first)

## Admin Access

Click the **Admin Login** button in the nav bar.

- **Password:** `SRCCAdmin@2025`

In admin mode you can:
- Inline-edit any text
- Click the profile photo to upload a new one
- Add / edit / delete cards, timeline entries, publications, awards, MoUs
- Upload gallery photos
- Update social links
- Save all changes to `localStorage`
- Export data as JSON
- Reset to default

## Tech Stack

- HTML5 + CSS3 + Vanilla JavaScript
- Google Fonts: Playfair Display + Source Sans 3
- Font Awesome 6.5 (via CDN)
- No build tools required

## Running Locally

Just open `index.html` in any modern browser — no server needed.

> This static portfolio runs without the backend API. Admin edit mode is enabled locally by entering the admin password in the login modal.
+
+If you want the full backend-based experience instead, see the top-level `README.md` and use the `backend` service.
+
+## Deploying

This is a static site. It works on GitHub Pages, Netlify, Vercel, Cloudflare Pages, or any static host.

### GitHub Pages
1. Push to a GitHub repository
2. Go to **Settings → Pages**
3. Source: **Deploy from a branch**, Branch: **main** / root
4. Save, and the site goes live at `https://<username>.github.io/<repo>/`

## License

All rights reserved. Content courtesy of Dr. Mallika Kumar.
