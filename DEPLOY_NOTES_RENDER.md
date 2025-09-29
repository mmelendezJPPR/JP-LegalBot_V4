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

