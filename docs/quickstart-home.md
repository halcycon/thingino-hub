# Quick Start Guide (Home Setup)

Get your Thingino Hub running in 5 minutes.

## What You'll Need

- **MQTT broker** – running somewhere on your network (or the same machine as the hub)
- **Telegram bot token** (optional, but helpful for remote access)
- **At least one Thingino camera** on the same network

---

## Step 1: Set Up Telegram Bot (Optional)

If you want to control cameras via Telegram:

1. Open Telegram and message `@BotFather`
2. Send `/newbot`
3. Choose a name and username for your bot
4. Copy the bot token (you'll use this in step 2)

**Skip this if you only want the web dashboard.**

---

## Step 2: Configure the Hub

```sh
cp config.example.yaml config.yaml
```

Open `config.yaml` in a text editor and set these values:

- **`mqtt.host`** – IP address of your MQTT broker (required)
  - Example: `"192.168.1.10"`
  - On the same machine as the hub? Use: `"host.containers.internal"`
- **`telegram.token`** – paste your bot token (optional, leave empty to skip)
  - Example: `"123456789:ABCDefGHiJKlmnoPQRstuvWXYZ"`

If your MQTT broker needs authentication:

```yaml
mqtt:
  host: "192.168.1.10"
  username: "mqtt-user"
  password: "mqtt-password"
```

---

## Step 3: Start the Hub

```sh
sh run-podman.sh
```

The script will:
- Build the container (`localhost/thinginohub:latest`)
- Start it in the background
- Publish the web dashboard at `http://127.0.0.1:8080`

**Updating code?** Skip the rebuild with:

```sh
SKIP_BUILD=1 sh run-podman.sh
```

---

## Step 4: Verify It's Working

Open your browser and go to: `http://127.0.0.1:8080`

You should see:
- ✅ MQTT broker status (green = connected)
- ✅ Telegram bot status (if configured)
- ✅ An empty camera roster (you'll add cameras next)

If you set up Telegram, send these commands to your bot:
- `/help` – bot should respond
- `/cam list` – should say "No cameras" (for now)

---

## Step 5: Connect Your First Camera

1. Open the web dashboard (if not already open)
2. Click the **"/enroll"** link or button
3. Enter your camera's IP address (e.g., `192.168.1.50`)
4. Enter ONVIF credentials (usually `thingino` / `thingino` for Thingino cameras)
5. Click "Connect"

The hub will pair with the camera and add it to your roster.

---

## What's Next?

- **Need to adjust settings?** Read [Configuration Reference](configuration.md)
- **Deploying to a server or NAS?** See [Deployment Guide](deployment-and-runtime.md)
- **Want to learn the web interface?** Check [Web UI Guide](web-ui.md)
- **Troubleshooting?** See [Operations Guide](operations.md)
