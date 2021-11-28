#!/bin/bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Invalid number of arguments"
    echo "./scripts/create_database.sh <NAMESPACE>"
    exit 1
fi

if [[ -z "${DATABASE_USERNAME}" ]]; then
    echo "Environment variable DATABASE_USERNAME not set"
    exit 1
fi

if [[ -z "${DATABASE_PASSWORD}" ]]; then
    echo "Environment variable DATABASE_PASSWORD not set"
    exit 1
fi

NAMESPACE="$1"

DATABASE_USERNAME_BASE64="$(echo -n "${DATABASE_USERNAME}" | base64)"
DATABASE_PASSWORD_BASE64="$(echo -n "${DATABASE_PASSWORD}" | base64)"

cat <<EOF | kubectl --namespace "${NAMESPACE}" apply -f -
apiVersion: v1
kind: Service
metadata:
  name: connect4-database
  labels:
    app: connect4-database
spec:
  ports:
  - port: 5432
    name: connect4-database
  type: NodePort 
  selector:
    app: connect4-database
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: connect4-database
  labels:
    app: connect4-database
spec:
  serviceName: "connect4-database"
  replicas: 1
  selector:
    matchLabels:
      app: connect4-database
  template:
    metadata:
      labels:
        app: connect4-database
    spec:
      containers:
      - name: connect4-database
        image: postgres:13-alpine
        envFrom:
        - configMapRef:
            name: connect4-database
        - secretRef:
            name: connect4-database
        ports:
        - containerPort: 5432
          name: postgresdb
        volumeMounts:
        - name: connect4-database
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: connect4-database
        persistentVolumeClaim:
          claimName: connect4-database
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: connect4-database
spec:
  storageClassName: microk8s-hostpath
  capacity:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 250Mi
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: connect4-database
  labels:
    app: connect4-database
data:
  POSTGRES_DB: connect4
---
apiVersion: v1
kind: Secret
metadata:
  name: connect4-database
  labels:
    app: connect4-database
data:
  POSTGRES_USER: "${DATABASE_USERNAME_BASE64}"
  POSTGRES_PASSWORD: "${DATABASE_PASSWORD_BASE64}"
EOF
