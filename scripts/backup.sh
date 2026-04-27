#!/bin/bash
BACKUP_DIR="/home/ubuntu/ai-tools-compare/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="aitc_db_${TIMESTAMP}.sql.gz"

docker exec aitc-postgres pg_dump -U aitc aitc_db | gzip > "${BACKUP_DIR}/${FILENAME}"

# Keep only last 7 days of backups
find "${BACKUP_DIR}" -name "aitc_db_*.sql.gz" -mtime +7 -delete

echo "[$(date)] Backup created: ${FILENAME}"
