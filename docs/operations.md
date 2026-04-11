# Operations and Troubleshooting

How to maintain, test, and troubleshoot your Thingino Hub.

---

## Testing

### Run Web Route Tests

Quick regression tests for the web interface:

```sh
python -m unittest -v tests.test_web_routes
```

### Run Full Test Suite

```sh
pytest -q
```

---

## Access Control

### Restrict Telegram Access

By default, anyone who knows your bot token can send commands. Restrict access:

```yaml
telegram:
  allowed_chat_ids:
    - 123456789      # Your Telegram chat ID
    - 987654321      # Another authorized user

  allowed_usernames:
    - "alice"        # Allow by username
    - "bob"
```

**Get your chat ID:**
- Send any message to your bot
- Check hub logs for the chat ID
- Or use a Telegram bot that echoes your chat ID

If both lists are empty, anyone who can message the bot is allowed.

---

## Available Commands

These commands are available via Telegram and the web UI:

- **`ping`** – Check if camera is responsive
- **`help`** – List available commands
- **`arm`** – Enable recording/monitoring
- **`disarm`** – Disable recording/monitoring
- **`snap`** – Take a snapshot and send to Telegram
- **`clip`** – Record a video clip and send to Telegram

---

## Common Issues and Solutions

### Bot doesn't reply to Telegram messages

**Check:**
1. Is your `telegram.token` correct?
2. Is only one instance of the hub running? (Multiple instances polling the same token will conflict)
3. Test with `/help` command

**Solution:**
- Verify token in `config.yaml`
- Check hub logs: `LOG_LEVEL=DEBUG sh run-podman.sh`
- Stop other instances: `podman ps` and `podman stop <container-id>`

### Commands acknowledged but camera does nothing

**Check:**
1. Is the MQTT broker running and reachable?
2. Is the camera subscribed to its command topic? (`thingino/cam/<camera_id>/cmd`)
3. Can the camera parse the command?
4. Has the camera been connected to the hub?

**Solution:**
- Verify `mqtt.host` in configuration
- Check camera logs for MQTT connection errors
- Use `/enroll` page to properly pair the camera
- Run `Rescan Cameras` in the dashboard

### Replies don't reach Telegram

**Check:**
1. Is the camera publishing to the correct reply topic? (`thingino/cam/<camera_id>/reply`)
2. Does the camera include the `request_id` in the reply JSON?
3. Is the chat ID mapped correctly?

**Solution:**
- Check camera logs for MQTT publish errors
- Verify reply JSON includes `request_id` field
- Check hub logs for missing chat mappings

### MQTT works on host but not in container

**Problem:** Podman container can't reach your local MQTT broker.

**Solution:** Use `host.containers.internal` for the MQTT host:

```yaml
mqtt:
  host: "host.containers.internal"
```

This special DNS name allows Podman containers to reach services running on the host.

### Dashboard won't load

**Check:**
1. Is the hub container running? `podman ps`
2. Is the web UI listening on the right port? (default: `8080`)
3. Are there startup errors in the logs?

**Solution:**
```sh
# Check if running
podman ps

# View logs
podman logs <container-id>

# Restart
SKIP_BUILD=1 sh run-podman.sh
```

### Snapshots not loading or outdated

**Check:**
1. Can you reach the camera directly? (Test URL in browser: `http://<ip>/x/ch0.jpg`)
2. Are credentials correct for HTTPS cameras?
3. Is snapshot URL correct?

**Solution:**
- Verify snapshot URL in configuration
- For HTTPS cameras, ensure `onvif_username` and `onvif_password` are set
- Manually refresh: Click "Refresh" on camera card
- Check hub logs for snapshot errors

### Camera won't pair

**Check:**
1. Is the camera on the same network?
2. Are ONVIF credentials correct? (Usually `thingino` / `thingino`)
3. Can you reach the ONVIF endpoint? (Try: `http://<camera-ip>/onvif/device_service`)

**Solution:**
- Verify camera IP address
- Confirm ONVIF credentials
- Test ONVIF endpoint in browser
- Check hub logs for pairing errors
- Restart the camera

---

## Viewing Logs

### In Docker/Podman

```sh
podman logs -f <container-id>
```

### From CLI (non-containerized)

Logs print to stdout when running directly.

### Enable Debug Logging

```sh
LOG_LEVEL=DEBUG sh run-podman.sh
```

---

## Database Maintenance

### History Database

Camera actions are stored in SQLite. To inspect:

```sh
sqlite3 hub-history.sqlite3
```

Common queries:
```sql
-- Recent actions
SELECT * FROM actions ORDER BY timestamp DESC LIMIT 20;

-- Actions for a specific camera
SELECT * FROM actions WHERE camera_id = 'aabbccddeeff';
```

---

## Performance Tips

- **Large number of cameras?** Increase snapshot heartbeat interval to reduce MQTT traffic
- **Slow snapshots?** Check camera upload bandwidth and network latency
- **High CPU usage?** Enable debug logging to identify bottlenecks

---

## Getting Help

- **Check the logs** – They usually explain what went wrong
- **Read configuration docs** – See [Configuration Reference](configuration.md)
- **Review camera setup** – See [Camera Setup Guide](camera-setup-and-pairing.md)
- **Understand MQTT flow** – See [MQTT Protocol Guide](mqtt-protocol.md)
