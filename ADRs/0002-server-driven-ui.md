# ADR-0002: Server-Driven UI with HTMX over React/Next.js

## Status
Accepted

## Context
We need to choose a frontend architecture for the MCP Control Center. The UI must be:
- Fast and responsive
- Mobile-friendly (iPhone/iPad)
- Work offline (PWA)
- Easy to develop and maintain
- Minimal JavaScript complexity

## Decision
Use server-driven UI with:
- **Jinja2** templates for HTML generation
- **HTMX** for dynamic updates without full page reloads
- **Alpine.js** for minimal client-side interactivity
- **Tailwind CSS** for styling

Reject React, Next.js, and other SPA frameworks.

## Consequences

### Positive
- **Simplicity**: Less JavaScript to write and maintain
- **Performance**: Fast initial page loads, smaller bundle sizes
- **SEO**: Server-rendered HTML, no hydration issues
- **Development Speed**: Faster iteration with templates
- **Progressive Enhancement**: Works without JavaScript
- **Less Complexity**: No build tools, no state management
- **Offline**: Service worker caches HTML pages easily

### Negative
- **Limited Interactivity**: Complex UI interactions harder
- **Learning Curve**: Team needs to learn HTMX paradigm
- **Ecosystem**: Smaller than React ecosystem
- **Components**: No JSX-style component model

### Neutral
- Different mental model than SPA
- Some duplication between backend and templates

## Alternatives Considered

### React + Next.js
- **Pros**: Large ecosystem, rich components, familiar to many
- **Cons**: Heavy bundle, build complexity, SEO challenges, hydration issues
- **Verdict**: Rejected - too complex for our needs

### Vue.js
- **Pros**: Progressive framework, good DX, smaller than React
- **Cons**: Still SPA complexity, build tools required
- **Verdict**: Rejected - prefer server-driven approach

### Svelte/SvelteKit
- **Pros**: Compiler-based, small bundles, good DX
- **Cons**: Smaller ecosystem, still SPA complexity
- **Verdict**: Rejected - prefer simpler approach

### Plain Server-Rendered HTML
- **Pros**: Simplest possible approach
- **Cons**: No dynamic updates without full page reloads
- **Verdict**: Rejected - need some interactivity

## Implementation Notes

### HTMX Usage
- `hx-get`, `hx-post` for dynamic content loading
- `hx-swap` for partial page updates
- `hx-trigger` for event-driven updates
- `hx-target` for specifying update location

### Alpine.js Usage
- Dropdown menus
- Modal dialogs
- Form validation
- Simple state management

### Tailwind CSS
- Utility-first styling
- Mobile-first responsive design
- Dark mode support (future)
- Custom design system

### Progressive Enhancement
1. Core functionality works without JavaScript
2. HTMX enhances with dynamic updates
3. Alpine.js adds interactive flourishes
4. Service worker enables offline

## Mobile Considerations
- Touch-friendly tap targets (min 44px)
- Swipe gestures with Alpine.js
- Sticky action bars
- Bottom navigation on mobile
- PWA installation prompts

## References
- [HTMX Documentation](https://htmx.org/)
- [Alpine.js Documentation](https://alpinejs.dev/)
- [The Simplicity of Server-Driven UI](https://htmx.org/essays/)
