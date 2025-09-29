Render deployment notes for JP-LegalBot

Problem: When you deploy to Render using the default setup, conversations are stored in a SQLite file under `database/conversaciones.db` inside the container filesystem. Render's web services containers are ephemeral: unless you use a managed DB or a persistent disk (Render Persistent Disks available on paid plans), the file will not survive redeploys or multiple instances. That explains why "the bot doesn't remember conversations" when deployed.

What to do (3 options, ordered by recommended robustness):

1) Use a managed database (recommended)
   - Provision a managed Postgres (Render Postgres, AWS RDS, Azure Database for Postgres, etc.).
   - Set DATABASE_URL environment variable in Render to the Postgres connection string, e.g.:
     DATABASE_URL=postgres://user:pass@host:5432/jp_legalbot
   - The app will detect a non-sqlite DATABASE_URL and skip creating local sqlite files. Modify later to use SQLAlchemy if you want full compatibility.

2) Use Render Persistent Disk (if available on your plan)
   - Create a Persistent Disk in the same region and attach it to your service.
   - Set CONVERSACIONES_DB to a sqlite path on the mounted disk (absolute path), for example:
     CONVERSACIONES_DB=/mnt/data/conversaciones.db
   - Or set DATABASE_URL=sqlite:////mnt/data/conversaciones.db
   - The app respects `CONVERSACIONES_DB` and `DATABASE_URL` for sqlite paths.

3) Keep SQLite inside container (development only)
   - This will not persist across deploys. Use only for demos.

Environment variables the app supports (important ones):
- CONVERSACIONES_DB  -> path or sqlite:/// URL to conversations DB (preferred)
- DATABASE_URL       -> Postgres/MySQL or sqlite:/// URL (fallback used by several modules)
- DB_PATH            -> path for hybrid_knowledge.db (used by ai_system and app)

Quick checklist to configure on Render dashboard (Environment):
- Add `DATABASE_URL` or `CONVERSACIONES_DB` (see examples above)
- Add `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_DEPLOYMENT_NAME`, `AZURE_OPENAI_API_VERSION`
- Add `SECRET_KEY` (>= 16 chars)
- PORT (Render sets this automatically, but app respects PORT env var)

Verification steps after deploy:
- Visit `/test-endpoint` if available or open the web UI and perform a chat.
- Re-deploy a new version and confirm the conversation persists.

Notes and security:
- Do not commit secrets to the repo or screenshots with keys.
- If using managed Postgres, ensure network rules allow Render to connect.

If you want, I can:
- Add a small startup check endpoint that returns which DB path is active and whether it is sqlite vs external DB.
- Add automatic migration to create tables in Postgres (requires SQLAlchemy).

Additional instructions: using `/ensure-schema` and environment variables

- New environment variables supported by the app (optional):
   - `ADMIN_SCHEMA_TOKEN` -> secret token required to apply schema changes via `/ensure-schema`.
   - `ENSURE_SCHEMA_ON_STARTUP` -> set to `1` to attempt schema ensure automatically at process start (optional, idempotent).

How to run the schema ensure endpoint (recommended flow)

1) Diagnostic: check which DB paths the running service is using

    PowerShell:

    ```powershell
    Invoke-RestMethod -Uri "https://YOUR_RENDER_URL/ensure-schema" -Method GET
    ```

    The response will contain the resolved `conversaciones` and `hybrid` paths the service will operate on.

2) Apply schema (idempotent) — use ADMIN_SCHEMA_TOKEN for safety

    - Set an environment variable in Render: `ADMIN_SCHEMA_TOKEN` to a strong secret (example: `s3cr3t-ensure-schema`).

    - Then run (PowerShell examples):

    GET with token in query (simple):

    ```powershell
    $token = 's3cr3t-ensure-schema'
    Invoke-RestMethod -Uri "https://YOUR_RENDER_URL/ensure-schema?apply=1&token=$token" -Method GET
    ```

    POST with header (preferred):

    ```powershell
    $headers = @{ 'X-ADMIN-TOKEN' = 's3cr3t-ensure-schema' }
    Invoke-RestMethod -Uri "https://YOUR_RENDER_URL/ensure-schema" -Method POST -Headers $headers
    ```

    The service will reply with JSON containing messages about tables/columns created or warnings (for example if FTS5 is not available in the sqlite build).

Notes and troubleshooting

- If the response contains a warning like `could not create fts_chunks (FTS5 available?): ...`, it means the Python / SQLite binary running in the container lacks FTS5 support. Fixes:
   - Use a Python runtime with FTS5 enabled, or
   - Use a managed vector/FTS service instead of SQLite FTS.

- If you prefer automatic application at startup, set `ENSURE_SCHEMA_ON_STARTUP=1` in the service env. The app will attempt to ensure the schema at boot; logs will show the results. This is idempotent but for safety consider keeping `ENSURE_SCHEMA_ON_STARTUP=0` and running the endpoint manually the first time.

Security

- Keep `ADMIN_SCHEMA_TOKEN` secret and rotate it if shared.
- Do not expose `/ensure-schema` to the public without a token. The endpoint will reject apply requests if `ADMIN_SCHEMA_TOKEN` is set and the provided token is missing or invalid.

