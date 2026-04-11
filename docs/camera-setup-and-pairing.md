# Camera Setup and Pairing

How cameras connect to Thingino Hub and how the pairing process works.

---

## How It Works

Cameras running Thingino firmware publish information to your MQTT broker, and the hub listens for these broadcasts. Here's the flow:

1. **Camera registers itself** – Publishes a "hello" message with its ID and details
2. **Hub discovers camera** – Sees the registration and adds it to the roster
3. **You connect via web UI** – Click "Connect" or use the `/enroll` page
4. **Hub pairs with camera** – Sends pairing credentials over MQTT
5. **Camera receives credentials** – Updates its config with hub connection details
6. **Communication established** – Camera can now receive commands from the hub

---

## What the Hub Needs from a Camera

For each camera, the hub needs:

- **Camera ID** – Unique identifier (MAC address or similar)
- **Name** – Friendly display name
- **IP Address** – Where to reach the camera
- **ONVIF Endpoint** – For device discovery and control (usually `http://<ip>/onvif/device_service`)
- **ONVIF Credentials** – Username and password (default: `thingino` / `thingino`)
- **Snapshot URL** – Where to grab a still image (e.g., `http://<ip>/x/ch0.jpg`)

---

## Camera-Side Setup (What Thingino Firmware Does)

Thingino cameras automatically:

1. **Subscribe to command topic:**
   ```
   thingino/cam/<camera_id>/cmd
   ```

2. **Publish registration (retained) to:**
   ```
   thingino/cam/<camera_id>/hello
   ```

3. **Accept pairing commands** with hub connection details (MQTT broker address, port, credentials)

4. **Publish replies to:**
   ```
   thingino/cam/<camera_id>/reply
   ```

---

## Auto-Registration

Cameras send a retained MQTT message with their details:

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

The hub subscribes to these messages and builds its camera roster automatically.

---

## Manual Camera Setup (If Auto-Discovery Fails)

If your camera doesn't auto-register, you can manually configure it in `config.yaml`:

```yaml
cameras:
  - id: "aabbccddeeff"
    name: "front-door"
    snapshot_url: "http://192.168.1.50/x/ch0.jpg"
    onvif_endpoint: "http://192.168.1.50/onvif/device_service"
    onvif_username: "thingino"
    onvif_password: "thingino"
```

---

## Snapshot Sources

Different camera models expose snapshots differently:

**Standard snapshots (most cameras):**
- URL: `http://<camera-ip>/x/ch0.jpg`
- Channel: `ch0` (main), `ch1` (substream), etc.

**Raptor cameras (HTTPS with authentication):**
- URL: `https://<camera-ip>:8443/snap.jpg`
- Port: 8443
- Requires ONVIF credentials

---

## Media Commands

### Snapshots (`snap`)
- **Hub-driven**: Hub fetches image directly from the camera
- **Display**: Image is posted to Telegram or shown in the dashboard

### Clips (`clip`)
- **Camera-driven**: Camera records a clip and sends it to Telegram
- **Setup**: Camera must have `send2telegram` utility configured

---

## Camera IDs

The authoritative camera ID comes from the MQTT topic path:

```
thingino/cam/<camera_id>/hello
thingino/cam/<camera_id>/cmd
```

**Use camera MAC address or serial number** — don't mix in legacy CGI IDs or other identifiers.

---

## Troubleshooting

**Camera doesn't appear in the roster?**
- Verify camera is on the same network as the hub
- Check MQTT broker is running and reachable
- Confirm camera has Thingino firmware with MQTT support
- Check camera logs for MQTT connection errors

**Can't pair the camera?**
- Verify ONVIF credentials are correct (usually `thingino` / `thingino`)
- Confirm ONVIF endpoint is accessible (usually `http://<ip>/onvif/device_service`)
- Check hub logs for pairing errors

**Snapshots not loading?**
- Test snapshot URL directly in browser: `http://<camera-ip>/x/ch0.jpg`
- For HTTPS cameras, verify credentials in configuration
- Check camera firewall allows hub access

---

## Next Steps

- **Start pairing?** Go to the web dashboard `/enroll` page
- **Need MQTT help?** Read [MQTT Protocol Guide](mqtt-protocol.md)
- **Advanced setup?** See [Configuration Reference](configuration.md)
