# Web Search Examples

Use `exa.web_search_exa` for news, current events, product comparisons, and general web lookup.

```bash
mcporter call 'exa.web_search_exa(query: "latest AI breakthroughs 2026", numResults: 5)'
mcporter call 'exa.web_search_exa(query: "quantum computing news", type: "fast")'
mcporter call 'exa.web_search_exa(query: "how does RAG work in LLMs", type: "deep", numResults: 8)'
mcporter call 'exa.web_search_exa(query: "best practices for API design", numResults: 5)'
mcporter call 'exa.web_search_exa(query: "M4 Mac Mini specifications and reviews")'
mcporter call 'exa.web_search_exa(query: "comparison of vector databases", type: "deep")'
```

Parameter guidance:

- `type: "auto"` is the default balanced mode
- `type: "fast"` is best for quick lookup
- `type: "deep"` is best for thorough research
- `numResults: 3-5` for a focused answer
- `numResults: 5-8` for standard research

