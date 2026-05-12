| Task | Status | Owner | Notes |
|---|---|---|---|
| Auth API | 🚧 | Sam | Waiting on OAuth flow |
| Billing | ✅ | Alex | Shipped |

- [ ] task 1
- [x] task 2

<details>
<summary>Implementation notes</summary>

Detailed notes here.

</details>


flowchart TD
    A[Developer Builds Docker Image] --> B[Docker Image]
    B --> C[Developer Laptop]
    B --> D[QA Server]
    B --> E[Production Server]

    C --> F[Same Container]
    D --> F
    E --> F