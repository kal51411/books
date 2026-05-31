# API Documentation

## `POST /api/v1/ask`

Request:

```json
{ "query": "Can police arrest without warrant?", "mode": "research" }
```

Response includes:

- `answer`
- `confidence`
- `citations[]`
- `evidence[]`
- `caveats[]`

The endpoint returns `422` if prompt injection is detected, no evidence is retrieved, or citation validation fails.
