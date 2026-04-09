---
name: web-scraper-as-a-service
description: Build client-ready web scrapers with clean data output. Use when creating scrapers for clients, extracting data from websites, or delivering scraping projects.
---

## When to use
- A user wants a scraping solution built from a brief or URL.
- The target site needs structured extraction, cleaning, and packaging for handoff.
- The work includes generating code, running the scraper, and delivering client-ready outputs.

## Inputs
- Target URL, site brief, or scraping requirements.
- Requested fields, output format, and delivery constraints.
- Notes about pagination, login, anti-bot protection, or allowed data scope.

## Outputs
- A `scraper/` directory with `scrape.py`, `requirements.txt`, `config.json`, and client setup docs.
- A `delivery/` package with cleaned data, quality notes, and handoff documentation.
- A short summary with record counts, data quality, and file locations.

## Tool dependencies
- `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash`, `WebFetch`, `WebSearch`
- Use `requests` + `BeautifulSoup` for static pages.
- Use `playwright` for JavaScript-rendered pages.
- Use direct API calls when a site exposes usable network endpoints.

## Stop conditions
- The target cannot be identified clearly enough to scrape safely.
- Robots.txt or terms of service prohibit the requested collection.
- The page is blocked by CAPTCHA or anti-bot controls and no permitted fallback exists.
- The user asks for personal data extraction without explicit authorization.

## Instructions
1. Analyze the target before writing code.
   - Check whether the site is static HTML or client-rendered.
   - Identify visible anti-scraping measures, pagination, and the expected data shape.
   - Estimate the number of pages or records.
2. Choose the simplest viable extraction method.
   - Static HTML: `requests` + `BeautifulSoup`.
   - JavaScript-rendered: `playwright`.
   - API available: call the API directly.
3. Build the scraper as a complete project.
   - Keep configuration in `config.json`.
   - Include rate limiting, retries, user-agent rotation, progress output, and incremental writes.
   - Save errors to a log instead of crashing on a single bad page.
4. Clean and validate the data.
   - Remove duplicates.
   - Normalize whitespace, encoding, and formats.
   - Validate required fields, numbers, and URLs.
   - Produce a brief quality report.
5. Package the client deliverable.
   - Provide cleaned data in the requested format.
   - Include a README and a scraper explanation.
   - Note known limits and how to rerun the scraper.
6. Follow the ethical scraping rules.
   - Respect robots.txt.
   - Rate limit by at least 2 seconds between requests.
   - Use an honest user agent.
   - Avoid scraping personal data unless the client explicitly authorizes it and the data is public.
   - Cache responses and avoid unnecessary re-scrapes.
