# Deployment and Runtime

How to run Thingino Hub in different environments.

---

## Docker/Podman (Recommended)

### Quick Start

```sh
sh run-podman.sh
```

This helper script:
1. Builds the container image (`localhost/thinginohub:latest`)
2. Mounts `config.yaml` so the hub reads your settings
3. Mounts `./data/` for persistent camera state
4. Publishes the web UI on `http://127.0.0.1:8080`
5. Runs in the background

**Skip the rebuild (if code hasn't changed):**
```sh
SKIP_BUILD=1 sh run-podman.sh
```

### Manual Build and Run

```sh
podman build -t localhost/thinginohub:latest -f Containerfile .

podman run -d \
  -p 8080:8080 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -v $(pwd)/data:/app/data \
  localhost/thinginohub:latest
```

### Docker Compose

```sh
podman compose up --build
```

---

## Podman Tips for Local MQTT Broker

If your MQTT broker is running on the same machine as Podman (but outside the container):

```yaml
mqtt:
  host: "host.containers.internal"
```

This special DNS name lets the container reach services on the host machine.

---

## Run Without Containers

For development or troubleshooting, run directly on your machine:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

HUB_CONFIG=$(pwd)/config.yaml python3 -m app.main
```

The hub will be available at `http://127.0.0.1:8080`.

---

## Storage and Persistence

### Camera State
- **File**: `data/camera-state.yaml` (inside container)
- **Contains**: Camera roster, metadata, connection status
- **Persists**: Across restarts

### History Database
- **Default**: `hub-history.sqlite3` (next to `config.yaml`)
- **Contains**: Log of all actions, commands, errors
- **Override** with environment variable:
  ```sh
  export HUB_HISTORY_DB=/custom/path/hub-history.sqlite3
  ```

---

## Environment Variables

Override settings without editing config files:

```sh
# Configuration file location
export HUB_CONFIG=/path/to/config.yaml

# History database location
export HUB_HISTORY_DB=/path/to/hub-history.sqlite3

# Camera state persistence location
export HUB_STATE_PATH=/path/to/camera-state.yaml

# Logging level
export LOG_LEVEL=DEBUG
```

**Common log levels**: `DEBUG`, `INFO`, `WARNING`, `ERROR`

---

## Debugging with Logs

View detailed logs while running:

```sh
LOG_LEVEL=DEBUG sh run-podman.sh
```

**In Docker Compose:**
```sh
LOG_LEVEL=DEBUG podman compose up --build
```

This helps troubleshoot MQTT connection issues, camera pairing problems, or Telegram bot issues.

---

## Production Deployments

### On a NAS or Server

1. **Clone the repository** to your NAS/server
2. **Configure** `config.yaml` with your MQTT broker and Telegram bot
3. **Use Docker Compose** for easier management:
   ```sh
   podman compose up -d
   ```
4. **Set up auto-restart** with systemd or your container orchestration tool

### Port Forwarding

By default, the hub listens on `127.0.0.1:8080` (localhost only). To expose it externally:

```sh
podman run -d \
  -p 0.0.0.0:8080:8080 \
  ...
```

**Security note:** Always use strong passwords if exposing the dashboard publicly.

### Reverse Proxy

For better security, use a reverse proxy (Nginx, Caddy, etc.):

```nginx
server {
    listen 443 ssl;
    server_name hub.example.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
    }
}
```

---

## Next Steps

- **Quick start at home?** See [Quick Start Guide](quickstart-home.md)
- **Configuration help?** Read [Configuration Reference](configuration.md)
- **Troubleshooting?** Check [Operations Guide](operations.md)
