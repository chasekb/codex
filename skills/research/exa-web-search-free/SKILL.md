---
name: exa-web-search-free
description: Free AI search via Exa MCP. Web search for news/info, code search for docs/examples from GitHub/StackOverflow, company research for business intel. No API key needed.
metadata:
  clawdbot:
    emoji: ""
    requires:
      bins:
        - mcporter
---

# Exa Web Search (Free)

Neural search for web, code, and company research. No API key required.

## Setup

Verify `mcporter` is configured:

```bash
mcporter list exa
```

If not listed:

```bash
mcporter config add exa https://mcp.exa.ai/mcp
```

## Web Search

Use this for current facts, news, market/product research, and general web lookup.

```bash
mcporter call 'exa.web_search_exa(query: "latest AI news 2026", numResults: 5)'
```

Parameters:
- `query` - Search query
- `numResults` (optional, default: 8)
- `type` (optional) - `"auto"`, `"fast"`, or `"deep"`

Reference examples: [web-search.md](references/web-search.md)

## Code Context Search

Use this for code examples, docs snippets, and API usage patterns from GitHub and Stack Overflow.

```bash
mcporter call 'exa.get_code_context_exa(query: "React hooks examples", tokensNum: 3000)'
```

Parameters:
- `query` - Code/API search query
- `tokensNum` (optional, default: 5000)
- Range: 1000-50000

Reference examples: [code-context.md](references/code-context.md)

## Company Research

Use this for company background, funding, competitive context, and business intelligence.

```bash
mcporter call 'exa.company_research_exa(companyName: "Anthropic", numResults: 3)'
```

Parameters:
- `companyName` - Company name
- `numResults` (optional, default: 5)

Reference examples: [company-research.md](references/company-research.md)

## Advanced Tools

Enable the full Exa toolset when you need deep search, crawling, people lookup, or staged research workflows.

- `web_search_advanced_exa`
- `deep_search_exa`
- `crawling_exa`
- `people_search_exa`
- `deep_researcher_start/check`

Enable all tools:

```bash
mcporter config add exa-full "https://mcp.exa.ai/mcp?tools=web_search_exa,web_search_advanced_exa,get_code_context_exa,deep_search_exa,crawling_exa,company_research_exa,people_search_exa,deep_researcher_start,deep_researcher_check"
# Then use:
mcporter call 'exa-full.deep_search_exa(query: "AI safety research")'
```

Reference examples: [advanced-tools.md](references/advanced-tools.md)

## Tips

- Web: Use `type: "fast"` for quick lookup, `"deep"` for thorough research
- Code: Lower `tokensNum` (1000-2000) for focused, higher (5000+) for comprehensive
- See the function-specific reference files under `references/` for more patterns

## Resources

- [GitHub](https://github.com/exa-labs/exa-mcp-server)
- [npm](https://www.npmjs.com/package/exa-mcp-server)
- [Docs](https://exa.ai/docs)
