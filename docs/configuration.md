# Configuration Reference

How to configure Thingino Hub to work with your cameras, MQTT broker, and Telegram bot.

## Configuration File

The hub reads settings from `config.yaml` (or set `HUB_CONFIG` environment variable).

---

## Essential Settings

### MQTT Broker (Required)

Your hub talks to cameras via MQTT. You need to tell it where to find your broker:

```yaml
mqtt:
  host: "192.168.1.10"
  port: 1883
  username: "mqtt-user"        # optional
  password: "mqtt-password"    # optional
  tls: false
```

**Common values:**
- **localhost** on the same machine: Use `"host.containers.internal"` (if running in Podman)
- **Network address**: Use the IP address (e.g., `"192.168.1.10"`)

### Telegram Bot (Optional)

If you want to control cameras via Telegram:

```yaml
telegram:
  token: "YOUR_BOT_TOKEN_HERE"
```

**Where to get your token:** Message `@BotFather` on Telegram, send `/newbot`, follow the prompts, and copy the token.

---

## Camera Settings (Optional)

You can pre-configure cameras or let the hub discover them automatically via MQTT.

**Manual camera entries:**

```yaml
cameras:
  - id: "aabbccddeeff"
    name: "front-door"
    snapshot_url: "http://192.168.1.50/x/ch0.jpg"
    onvif_endpoint: "http://192.168.1.50/onvif/device_service"
    onvif_username: "thingino"
    onvif_password: "thingino"
```

**Important fields:**
- `id` – camera's unique identifier (MAC address or similar)
- `name` – friendly name shown in the dashboard
- `snapshot_url` – URL to grab a still image from the camera
- `onvif_endpoint` – ONVIF device service URL (for pairing and control)

**Not sure about these values?** The hub can discover them automatically from MQTT registrations. You only need this if you prefer to hardcode camera details.

---

## Snapshot/Preview Options

Different camera models expose snapshots differently:

**Standard cameras (most Thingino models):**
```yaml
snapshot_url: "http://192.168.1.50/x/ch0.jpg"
```

**Raptor cameras (HTTPS, requires authentication):**
```yaml
snapshot_url: "https://192.168.1.50:8443/snap.jpg"
onvif_username: "thingino"
onvif_password: "thingino"
```

The hub will use these credentials automatically for authentication.

---

## Web Dashboard Security (Optional)

Protect your dashboard with a username and password:

**In YAML:**
```yaml
ui:
  username: "admin"
  password: "change-me"
```

**Via environment variables:**
```sh
export HUB_UI_USERNAME=admin
export HUB_UI_PASSWORD=change-me
```

---

## Advanced: MQTT Topics

If you need to customize MQTT topic names (usually not needed):

```yaml
routing:
  command_topic: "thingino/cam/{camera_id}/cmd"
  reply_topic: "thingino/cam/+/reply"
  registration_topic: "thingino/cam/+/hello"
```

---

## Advanced: History Database

Camera actions are logged to SQLite. Customize where:

```yaml
history:
  enabled: true
  db_path: "/path/to/hub-history.sqlite3"
```

Or set via environment:
```sh
export HUB_HISTORY_DB="/custom/path/hub-history.sqlite3"
```

---

## Minimal Example (Gets You Started)

```yaml
mqtt:
  host: "192.168.1.10"

telegram:
  token: "YOUR_BOT_TOKEN_HERE"
```

That's it! The hub will auto-discover cameras from MQTT registrations.

---

## Need Help?

- **Dashboard won't load?** Check that `mqtt.host` is correct
- **Telegram not working?** Verify your `telegram.token` and test with `/help`
- **Cameras not appearing?** See [Camera Setup Guide](camera-setup-and-pairing.md)
- **Confused about MQTT?** Read [MQTT Protocol Guide](mqtt-protocol.md)
