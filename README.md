# Thingino Hub

## What is Thingino Hub?

Thingino Hub is a **central control panel for your Thingino cameras**. If you have multiple security cameras around your home or property, this hub lets you:

- **See live previews** of all cameras in one place
- **Check camera settings** and status without visiting each camera's web interface
- **Send commands** to cameras (take a snapshot, arm/disarm, record a clip)
- **Get snapshots in Telegram** when you ask for them
- **Manage everything** through a simple web dashboard

Think of it as the "nerve center" for all your cameras — one place to monitor, control, and configure everything.

---

## Why Use Thingino Hub?

**Without a hub:** You have to log into each camera individually, remember different IP addresses, and manually trigger actions.

**With Thingino Hub:**
- One dashboard shows all cameras at once
- Control cameras via Telegram (no need to open a web browser)
- Automatic camera discovery — new cameras appear in the roster as they come online
- Secure pairing so cameras can talk to the hub without manual configuration
- View camera health, firmware version, and other metadata in one place

---

## Key Features

- **Web Dashboard** – Live camera roster with preview snapshots, status, and quick actions
- **Multi-Camera Support** – Handle dozens of cameras with automatic discovery
- **Telegram Integration** – Send commands and receive snapshots via Telegram bot
- **Camera Enrollment** – Easy connect/pair workflows with built-in credential validation
- **Snapshot Preview** – View the latest image from each camera (cached for fast loading)
- **Native API Support** – For cameras with Thingino's native API, get direct API control
- **History Tracking** – Local database of actions and camera state changes
- **Optional Web UI Auth** – Restrict dashboard access with username/password
- **MQTT-Based** – All camera communication happens over MQTT (secure, reliable)

---

## Quick Start

### Before You Start

You'll need:
- An MQTT broker running somewhere on your network (or this machine)
- A Telegram bot token (optional, but recommended for remote access)
- At least one Thingino camera on the same network

### 1. Create a Telegram Bot (Optional)

If you want to control cameras via Telegram:

1. Open Telegram and find `@BotFather`
2. Send `/newbot`
3. Choose a bot name and username
4. Copy the bot token

### 2. Set Up Configuration

```sh
cp config.example.yaml config.yaml
```

Edit `config.yaml` and set:

- **`telegram.token`** – paste your bot token (or leave empty to skip Telegram)
- **`mqtt.host`** – your MQTT broker's IP address (e.g., `192.168.1.10`)

If your MQTT broker is on the **same machine** as the hub:

```yaml
mqtt:
  host: "host.containers.internal"
```

### 3. Start the Hub

```sh
sh run-podman.sh
```

The hub will:
- Build a Docker container
- Start running in the background
- Expose the web dashboard on `http://127.0.0.1:8080`

### 4. Open the Dashboard

Go to `http://127.0.0.1:8080` in your browser.

You should see:
- Status of the Telegram bot and MQTT broker
- A roster of discovered cameras (if any are online)

### Optional: Enable FastAPI API v2 teaser

The hub now includes an optional FastAPI-powered teaser API that runs alongside the existing Flask UI with minimal disruption.

Set:

```sh
export HUB_API_V2_ENABLED=1
export HUB_API_V2_PORT=8090
```

Then restart the hub and open:

- `http://127.0.0.1:8090/api/v2/docs`
- `http://127.0.0.1:8090/api/v2/health`
- `http://127.0.0.1:8090/api/v2/cameras`

When this flag is enabled, selected camera-detail UI actions are routed through API v2 first, with automatic fallback to the existing Flask handler if API v2 is unavailable.

Practical teaser use case: quickly identify cameras that need operator attention:

```sh
curl -s "http://127.0.0.1:8090/api/v2/cameras/attention?minimum_severity=high&limit=10"
```

This endpoint surfaces cameras with actionable issues (offline state, API failures, incomplete setup, MQTT visibility/command problems) and returns suggested next actions.

Migration progress teaser: a first set of action endpoints is now available in API v2:

- `POST /api/v2/cameras/{camera_id}/hydrate`
- `POST /api/v2/cameras/{camera_id}/refresh/api`
- `POST /api/v2/cameras/{camera_id}/refresh/onvif`
- `POST /api/v2/cameras/{camera_id}/refresh/snapshot`
- `POST /api/v2/cameras/{camera_id}/service/{service_name}/{operation}`
- `POST /api/v2/cameras/{camera_id}/streaming/start`
- `POST /api/v2/cameras/{camera_id}/streaming/stop`
- `POST /api/v2/cameras/{camera_id}/streaming/restart`
- `POST /api/v2/cameras/{camera_id}/rescan`
- `POST /api/v2/cameras/{camera_id}/privacy`
- `POST /api/v2/cameras/{camera_id}/daynight`
- `POST /api/v2/cameras/{camera_id}/record`
- `POST /api/v2/cameras/{camera_id}/config/patch`
- `POST /api/v2/cameras/{camera_id}/apply-supported-config`
- `POST /api/v2/cameras/{camera_id}/send2-test/{service_name}`
- `POST /api/v2/enroll`
- `POST /api/v2/cameras/{camera_id}/connect`
- `POST /api/v2/bulk-action`
- `POST /api/v2/enroll/probe`
- `POST /api/v2/enroll/pairing-bundle`
- `POST /api/v2/enroll/pairing-install`
- `POST /api/v2/cameras/{camera_id}/pair`
- `POST /api/v2/cameras/{camera_id}/delete`

Example:

```sh
curl -sX POST "http://127.0.0.1:8090/api/v2/cameras/cam1/refresh/api"
```

```sh
curl -sX POST "http://127.0.0.1:8090/api/v2/cameras/cam1/service/streaming/restart"
```

```sh
curl -sX POST "http://127.0.0.1:8090/api/v2/cameras/cam1/daynight" \
  -H "Content-Type: application/json" \
  -d '{"mode":"night"}'
```

```sh
curl -sX POST "http://127.0.0.1:8090/api/v2/cameras/cam1/send2-test/telegram" \
  -H "Content-Type: application/json" \
  -d '{"verbose":true,"send_type":"photo"}'
```

```sh
curl -sX POST "http://127.0.0.1:8090/api/v2/cameras/cam1/pair"
```

```sh
curl -sX POST "http://127.0.0.1:8090/api/v2/enroll" \
  -H "Content-Type: application/json" \
  -d '{"camera_id":"cam1","ip":"192.168.1.10","onvif_username":"thingino","onvif_password":"thingino"}'
```

```sh
curl -sX POST "http://127.0.0.1:8090/api/v2/cameras/cam1/connect" \
  -H "Content-Type: application/json" \
  -d '{"onvif_username":"thingino","onvif_password":"thingino"}'
```

```sh
curl -sX POST "http://127.0.0.1:8090/api/v2/bulk-action" \
  -H "Content-Type: application/json" \
  -d '{"camera_ids":["cam1","cam2"],"action":"refresh-api"}'
```

Live validation checklist for newly started agents:

```sh
curl -s "http://127.0.0.1:8090/api/v2/cameras/cam1/payload"
```

Look for:
- `mqtt_command_capable: true`
- `present_on_mqtt_broker: true`
- `setup_status: pair` (before pair) or `setup_status: paired` (after pair)

### 5. Connect Your First Camera

1. Open the `/enroll` page in the dashboard
2. Enter your camera's IP address
3. Enter valid ONVIF credentials (usually `thingino` / `thingino`)
4. Click "Connect"

The hub will pair with the camera and add it to your roster.

---

## Next Steps

- **Learn about configuration:** [docs/configuration.md](docs/configuration.md)
- **Understand the web dashboard:** [docs/web-ui.md](docs/web-ui.md)
- **Set up cameras for pairing:** [docs/camera-setup-and-pairing.md](docs/camera-setup-and-pairing.md)
- **Deploy to production:** [docs/deployment-and-runtime.md](docs/deployment-and-runtime.md)
- **Troubleshoot issues:** [docs/operations.md](docs/operations.md)

---

## Full Documentation

- [quickstart-home.md](docs/quickstart-home.md) – Detailed home setup
- [configuration.md](docs/configuration.md) – All config options explained
- [deployment-and-runtime.md](docs/deployment-and-runtime.md) – Running in production, using Podman, env variables
- [web-ui.md](docs/web-ui.md) – Dashboard features and behavior
- [camera-setup-and-pairing.md](docs/camera-setup-and-pairing.md) – How camera pairing works
- [mqtt-protocol.md](docs/mqtt-protocol.md) – MQTT message format (for developers)
- [operations.md](docs/operations.md) – Running tests, troubleshooting, access control
- [ai-session-onboarding.md](docs/ai-session-onboarding.md) – For developers working on the hub itself
