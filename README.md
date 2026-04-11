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
