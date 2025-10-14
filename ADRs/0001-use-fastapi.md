# ADR-0001: Use FastAPI for REST API

## Status
Accepted

## Context
We need a modern Python web framework for building the MCP Control Center API. Requirements include:
- High performance and async support
- Automatic API documentation
- Type safety and validation
- Easy to learn and use
- Active community and ecosystem

## Decision
Use FastAPI as the web framework for the REST API.

## Consequences

### Positive
- **Performance**: FastAPI is one of the fastest Python frameworks (comparable to Node.js)
- **Type Safety**: Built-in Pydantic validation and type hints
- **Documentation**: Automatic OpenAPI/Swagger documentation
- **Modern**: Async/await support for concurrent operations
- **Developer Experience**: Excellent error messages and IDE support
- **Testing**: Easy to test with TestClient
- **Standards**: Based on OpenAPI and JSON Schema standards

### Negative
- **Learning Curve**: Team needs to learn async/await patterns
- **Maturity**: Younger than Flask/Django (but stable)
- **Ecosystem**: Smaller than Django (but growing rapidly)

### Neutral
- Requires Python 3.12+ (acceptable for our use case)
- Uvicorn required as ASGI server (standard practice)

## Alternatives Considered

### Flask
- **Pros**: Mature, large ecosystem, well-known
- **Cons**: Sync-only (without extensions), no automatic docs, less type safety
- **Verdict**: Rejected due to lack of async support and modern features

### Django + DRF
- **Pros**: Batteries included, mature, large ecosystem
- **Cons**: Heavy for our needs, ORM lock-in, slower performance
- **Verdict**: Rejected due to complexity and performance concerns

### Starlette
- **Pros**: Lightweight, async, fast
- **Cons**: Minimal features, requires more boilerplate, no automatic docs
- **Verdict**: Rejected - FastAPI builds on Starlette with better DX

## Implementation Notes
- Use Uvicorn as ASGI server
- SQLModel for ORM (built on Pydantic)
- Pydantic for request/response validation
- JWT for authentication (token-based in V1)

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python ASGI Frameworks Benchmark](https://www.techempower.com/benchmarks/)
