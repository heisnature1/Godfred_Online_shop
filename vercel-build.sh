#!/usr/bin/env bash
# Build script for Vercel deployments.
# Runs on every deploy: installs dependencies, collects static files,
# and applies database migrations.
set -euo pipefail

echo "▶ Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "▶ Applying database migrations..."
python manage.py migrate --no-input

echo "✅ Build complete."
