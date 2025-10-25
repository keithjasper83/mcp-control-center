# ADR-0003: GitHub Integration for Project Synchronization

## Status
Accepted

## Context
Users need a way to connect their existing GitHub repositories to the MCP Control Center without manual data entry. Additionally, when creating new projects, users want the option to automatically create a corresponding GitHub repository to maintain consistency between the control center and GitHub.

Requirements:
- Sync existing GitHub repositories as projects
- Automatically create GitHub repositories when creating new projects
- Maintain bidirectional awareness between Control Center and GitHub
- Support both personal and organization repositories
- Work with GitHub's REST API v3

## Decision
Implement GitHub integration as an optional feature with the following components:

1. **GitHub Service** (`app/services/github_service.py`)
   - Wrapper around GitHub REST API v3
   - Uses Personal Access Tokens for authentication
   - Methods for listing, creating, and querying repositories

2. **GitHub API Routes** (`app/api/github.py`)
   - `GET /api/github/config` - Check GitHub integration status
   - `GET /api/github/repositories` - List user's GitHub repositories
   - `POST /api/github/sync` - Sync all repositories as projects
   - `POST /api/github/repositories` - Create new repository and project

3. **Projects UI Enhancement**
   - "Sync from GitHub" button to import repositories
   - "Create GitHub repository" checkbox when creating projects
   - GitHub icon/link on project cards that have `repo_url`

4. **Configuration**
   - `GITHUB_TOKEN` environment variable for authentication
   - `GITHUB_SYNC_ENABLED` flag to enable/disable feature
   - Optional feature - works without GitHub token

## Consequences

### Positive
- **Seamless Integration**: Users can import all their GitHub repos in one click
- **Consistency**: New projects can automatically get GitHub repositories
- **Bidirectional Awareness**: Projects link back to their GitHub repos
- **Language Detection**: Automatically detect programming languages from GitHub API
- **Topics/Tags**: Import GitHub topics as project tags
- **Optional**: Feature gracefully degrades if no token provided

### Negative
- **Token Management**: Users must generate and manage GitHub Personal Access Token
- **API Rate Limits**: GitHub API has rate limits (5000 requests/hour for authenticated)
- **Token Permissions**: Requires `repo` scope which is relatively broad
- **Sync Complexity**: Need to handle conflicts if repo already exists
- **One-Way Sync**: Changes in Control Center don't sync back to GitHub

### Neutral
- Uses REST API v3 (stable but older than GraphQL API)
- Personal Access Tokens (classic) instead of GitHub Apps
- No webhook support for real-time sync (pull-based only)

## Alternatives Considered

### GitHub Apps
- **Pros**: Better security, webhook support, fine-grained permissions
- **Cons**: Complex setup, requires organization admin, OAuth flow needed
- **Verdict**: Rejected for V1 - too complex for initial implementation

### GraphQL API
- **Pros**: More efficient, modern, can fetch related data in one request
- **Cons**: More complex queries, less familiar to developers
- **Verdict**: Rejected - REST API v3 sufficient for our needs

### Two-Way Sync
- **Pros**: Changes in Control Center update GitHub
- **Cons**: Complex conflict resolution, requires webhooks, more error cases
- **Verdict**: Deferred to V2 - start with read + create pattern

### OAuth Flow
- **Pros**: Better user experience, no token management
- **Cons**: Requires web server callback URL, session management, more complex
- **Verdict**: Deferred to V2 - Personal Access Token simpler for now

## Implementation Notes

### Sync Strategy
When syncing from GitHub:
1. Fetch all repositories for authenticated user
2. For each repository:
   - Check if project with matching `repo_url` exists
   - If exists: update name and tags
   - If not exists: create new project with languages and topics
3. Return counts of synced/created projects

### Error Handling
- 401 errors: Display "GitHub token not configured" message
- 403 errors: Token lacks required permissions
- 404 errors: Repository not found or not accessible
- Rate limit errors: Display retry message with reset time

### Security Considerations
- Token stored in environment variable (not database)
- Token never exposed in API responses
- All GitHub API calls go through service layer
- No token in frontend JavaScript

## Future Enhancements (V2)
- GitHub Apps integration for better security
- Webhook support for real-time sync
- Two-way sync (Control Center → GitHub)
- Support for GitHub Enterprise
- Organization-level repository management
- Pull request integration
- Issue synchronization with Features

## References
- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub API Rate Limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
