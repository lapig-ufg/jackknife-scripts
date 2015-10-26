#!/bin/bash

ZBACKUP_DIR="/data/safe/ZBACKUP"
DATE=$(date "+%Y-%m-%d")
BACKUP_DIR="$ZBACKUP_DIR/backups$/DATE"

mkdir -p $BACKUP_DIR

tar -c "/data/lapig/GEO/PROJETOS/MOORE-FOUNDATION" | zbackup --silent backup $BACKUP_DIR/MOORE-FOUNDATION.tar
tar --exclude "/data/lapig/GEO/PROJETOS/PASTAGEM.ORG/PROCESSO/DADOS GEOGRÁFICOS/FONTE DE DADOS/" -c "/data/lapig/GEO/PROJETOS/PASTAGEM.ORG" | zbackup --silent backup $BACKUP_DIR/PASTAGEM.ORG.tar