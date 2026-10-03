# iOS Shortcut setup

This builds a Shortcut that appears in the share sheet of YouTube (and Safari) and saves the audio to Files.

You need the server from the main README running and reachable from your phone, plus your API token.

## Build the Shortcut

1. Open the **Shortcuts** app, tap **+** to create a new shortcut, and name it `Save Audio`.
2. Tap the info button (i) and turn on **Show in Share Sheet**. Under accepted types, keep only **URLs** (and **Safari web pages** if you want it from Safari).
3. Add these actions in order:

| # | Action | Settings |
|---|--------|----------|
| 1 | **Get URLs from** | Shortcut Input |
| 2 | **URL Encode** | Input: the URL from step 1 |
| 3 | **Text** | `https://YOUR-SERVER/audio?format=mp3&url=` then insert the **URL Encoded Text** variable from step 2 right after `url=` |
| 4 | **Get Contents of URL** | URL: the Text from step 3. Show More, Method: **GET**, Headers: add `X-API-Token` with your token |
| 5 | **Save File** | Turn off "Ask Where to Save" and pick a folder such as Files > Shortcuts > Audio |
| 6 | **Show Notification** | `Audio saved` |

4. Tap **Done**.

## Use it

In the YouTube app tap **Share**, scroll the share sheet to find **Save Audio** (tap **More** the first time and add it to Favourites), and tap it. Long videos can take a minute, so let the Shortcut finish.

## Troubleshooting

- **Nothing appears in the share sheet**: check that Show in Share Sheet is on and the accepted type includes URLs.
- **401 error**: the `X-API-Token` header is missing or does not match the server.
- **400 error**: the link was not recognised as a YouTube URL.
- **422 error**: yt-dlp could not fetch the video. Update the server's yt-dlp and retry.
- **Works on Wi-Fi but not on mobile data**: your server is only reachable on your home network. Use Tailscale or a tunnel.

## Prefer no server?

The main route needs no server at all: a-Shell runs yt-dlp on the phone. See [ios-on-device.md](ios-on-device.md).
