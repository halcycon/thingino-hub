# MQTT Protocol Guide

Understanding how cameras and the hub communicate via MQTT.

---

## Overview

Thingino Hub uses MQTT (a lightweight publish-subscribe protocol) to talk to cameras. Here's how it works:

1. **Hub sends commands** → publishes to `thingino/cam/<camera_id>/cmd`
2. **Camera receives** → subscribes to its command topic
3. **Camera executes** → performs the action (snapshot, arm, etc.)
4. **Camera replies** → publishes to `thingino/cam/<camera_id>/reply`
5. **Hub receives** → subscribes to all reply topics and sends response to Telegram

---

## Command Topic

Hub publishes commands to:

```
thingino/cam/<camera_id>/cmd
```

**Example payload:**

```json
{
  "request_id": "9b4a4aa8e4e6402f934e50c33402af90",
  "chat_id": 123456789,
  "username": "alice",
  "camera_id": "aabbccddeeff",
  "command": "snap",
  "args": [],
  "raw_text": "snap",
  "sent_at": 1710000000
}
```

**Important fields:**
- `request_id` – Unique ID for this command (camera includes in reply)
- `chat_id` – Telegram chat ID (where to send response)
- `command` – What to do: `ping`, `help`, `arm`, `disarm`, `snap`, `clip`
- `sent_at` – Unix timestamp when command was sent

---

## Reply Topic

Hub listens on:

```
thingino/cam/+/reply
```

The `+` means "any camera ID".

**Preferred reply format:**

```json
{
  "request_id": "9b4a4aa8e4e6402f934e50c33402af90",
  "message": "Snapshot queued"
}
```

**What the hub does:**
- Looks up the `request_id` to find the original chat ID
- Sends the `message` to Telegram
- Logs the action to the history database

**Other accepted formats:**
- Plain text (hub maps to chat using recent context)
- JSON with `chat_id` and `message` fields

---

## Registration Topic

Hub listens for camera registrations on:

```
thingino/cam/+/hello
```

**Example registration payload:**

```json
{
  "camera_id": "aabbccddeeff",
  "name": "front-door",
  "hostname": "front-door",
  "ip": "192.168.1.50",
  "snapshot_url": "http://192.168.1.50/x/ch0.jpg",
  "status": "online",
  "timestamp": 1710000000
}
```

**Important:**
- Cameras publish this as a **retained message** (persists on the broker)
- Hub subscribes on startup and auto-discovers cameras
- Metadata is used for the camera roster

---

## Customizing Topics

By default, topics follow the `thingino/cam/...` pattern. You can customize this in `config.yaml`:

```yaml
routing:
  command_topic: "thingino/cam/{camera_id}/cmd"
  reply_topic: "thingino/cam/+/reply"
  registration_topic: "thingino/cam/+/hello"
```

The `{camera_id}` placeholder is replaced with the actual camera ID.

---

## MQTT Broker Requirements

Your MQTT broker needs to support:

- **Retained messages** – Used by cameras to persist registrations
- **Wildcards** – Hub uses `+` and `#` in topic subscriptions
- **Basic authentication** (optional but recommended)
- **TLS/SSL** (recommended for security)

**Common brokers:**
- Mosquitto
- EMQX
- HiveMQ
- AWS IoT Core

---

## Debugging MQTT

### Monitor All Messages

```sh
mosquitto_sub -h <broker-ip> -t 'thingino/cam/#' -v
```

This shows all camera messages in real time (good for troubleshooting).

### Test Publishing

```sh
mosquitto_pub -h <broker-ip> -t 'thingino/cam/test-camera/cmd' -m '{"command":"ping"}'
```

### Check Retained Messages

```sh
mosquitto_sub -h <broker-ip> -t 'thingino/cam/+/hello' -v
```

Shows all camera registrations.

---

## Example: Complete Flow

Here's what happens when you send `/cam front-door snap` on Telegram:

1. **Hub receives Telegram message** → User sends `/cam front-door snap`
2. **Hub looks up camera** → Finds `front-door` camera ID: `aabbccddeeff`
3. **Hub publishes command** → Posts to `thingino/cam/aabbccddeeff/cmd` with:
   ```json
   {
     "request_id": "abc123",
     "chat_id": 12345,
     "command": "snap",
     ...
   }
   ```
4. **Camera receives** → Subscribes to `thingino/cam/aabbccddeeff/cmd`
5. **Camera takes snapshot** → Executes the command
6. **Camera replies** → Posts to `thingino/cam/aabbccddeeff/reply`:
   ```json
   {
     "request_id": "abc123",
     "message": "Snapshot: http://..."
   }
   ```
7. **Hub receives reply** → Looks up `request_id`, finds chat ID 12345
8. **Hub sends Telegram message** → Sends response to user

---

## Troubleshooting

**Hub not receiving camera replies?**
- Verify camera publishes to correct topic: `thingino/cam/<camera_id>/reply`
- Confirm `request_id` is included in reply JSON
- Check MQTT broker is functioning

**Messages not reaching cameras?**
- Verify MQTT broker is running
- Confirm cameras are subscribed to their command topic
- Check firewall allows MQTT traffic (port 1883 or 8883 for TLS)

**Hub not discovering cameras?**
- Verify cameras publish retained registration to `thingino/cam/<camera_id>/hello`
- Check MQTT broker supports retained messages
- Restart hub to re-subscribe to topics

---

## Next Steps

- **Configure MQTT** – See [Configuration Reference](configuration.md)
- **Set up cameras** – Read [Camera Setup Guide](camera-setup-and-pairing.md)
- **Troubleshoot** – Check [Operations Guide](operations.md)
