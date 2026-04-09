# Advanced Tools

Use the full Exa toolset when the basic search functions are not enough.

## Deep Search

```bash
mcporter call 'exa-full.deep_search_exa(query: "AI safety alignment research comprehensive overview")'
mcporter call 'exa-full.deep_search_exa(query: "climate change solutions technology innovation")'
```

## Advanced Web Search

```bash
mcporter call 'exa-full.web_search_advanced_exa(query: "machine learning tutorials", includeDomains: ["github.com", "arxiv.org"])'
mcporter call 'exa-full.web_search_advanced_exa(query: "AI developments", startPublishedDate: "2026-01-01")'
```

## Crawling

```bash
mcporter call 'exa-full.crawling_exa(url: "https://anthropic.com/news/claude-3-5-sonnet")'
mcporter call 'exa-full.crawling_exa(url: "https://example.com/article")'
```

## People Search

```bash
mcporter call 'exa-full.people_search_exa(query: "Yann LeCun AI researcher")'
mcporter call 'exa-full.people_search_exa(query: "Demis Hassabis DeepMind")'
```

## Deep Researcher

```bash
mcporter call 'exa-full.deep_researcher_start(topic: "quantum computing applications in cryptography", depth: "comprehensive")'
mcporter call 'exa-full.deep_researcher_check(taskId: "abc123")'
```
