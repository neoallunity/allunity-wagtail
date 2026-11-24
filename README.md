# AllUnity Wagtail

Wagtail rebuild of AllUnity.ru: page models, StreamField blocks, DRY templates, idempotent content migration, Docker/compose/nginx, and tests.

**Status:** working local/CI build; 27 pages render, migrations are reproducible. Deployment is not yet published — see `PLAN.md` and `STRATEGY.md` for the rollout decision.

## Quick start

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py migrate_data
python manage.py runserver
```

Docker: `docker compose up --build`.

## Checks

`check`, `makemigrations --check`, regression tests and migration reproducibility run in CI.

## License

MIT — see [LICENSE](LICENSE). Content migrated from AllUnity.ru may carry its own terms.
