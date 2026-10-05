# EasyAudio

**Save the audio of a YouTube video as an mp3 from your iPhone's Share button. Everything runs on your phone.**

![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Platform: iOS 14+](https://img.shields.io/badge/platform-iOS%2014%2B-lightgrey)
![No server](https://img.shields.io/badge/server-none-brightgreen)
![Status: beta](https://img.shields.io/badge/status-beta-orange)

Tap **Share** in YouTube, tap **Save Audio**, and an mp3 lands in your Files app. There is no server to host, no account to create and nothing to subscribe to.

<!-- Add a short screen recording here: docs/demo.gif -->

## Why this exists

Most "YouTube to mp3" options on iPhone are ad-filled websites, paid apps, or tools that need a computer or a server. EasyAudio takes a different route: it combines three free, open tools that already run on iOS, so the download and conversion happen on the device.

- **No server.** Nothing to host, nothing to keep running.
- **No account, no ads, no tracking.** This project collects no data.
- **Share-sheet workflow.** One tap from the video you are watching.
- **Real mp3 files.** Converted on the phone with ffmpeg.
- **Open source.** Small, readable and MIT licensed.

## How it works

```
YouTube Share  ->  Shortcut  ->  a-Shell mini  ->  mp3 in Files
                                 (yt-dlp + ffmpeg)
```

iOS does not let ordinary apps run arbitrary programs, but terminal apps can. [a-Shell mini](https://apps.apple.com/us/app/a-shell-mini/id1543537943) is a free terminal for iOS that includes Python and ffmpeg and can be driven from the Shortcuts app. [yt-dlp](https://github.com/yt-dlp/yt-dlp) runs inside it, ffmpeg converts the audio to mp3, and a small Shortcut passes in the link you shared.

## Requirements

- iPhone or iPad on iOS 14 or later
- About 400 MB of free space for a-Shell mini
- The free apps: [a-Shell mini](https://apps.apple.com/us/app/a-shell-mini/id1543537943) and Apple Shortcuts (built in)

## Install (about 5 minutes, once)

### 1. Install a-Shell mini

Get it from the App Store and open it once. You will see a black screen with a text line. That is the terminal, and it is normal.

### 2. Install the download tool

Copy these four lines, paste them into a-Shell mini and press return. Wait until the cursor comes back.

```
mkdir -p ~/Documents/bin
mkdir -p ~/Documents/Audio
curl -L -o ~/Documents/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp
chmod +x ~/Documents/bin/yt-dlp
```

This installs yt-dlp and creates a folder called **Audio** for your files.

### 3. Create the Save Audio shortcut

In the **Shortcuts** app:

1. Tap **+** to create a new shortcut.
2. Tap the name at the top, choose **Rename**, and type `Save Audio`.
3. Tap the **i** button and turn on **Show in Share Sheet**. Under **Share Sheet Types**, keep only **URLs**.
4. Tap **Add Action**, search for `Execute Command`, and choose the one from **a-Shell mini**.
5. In the command box, type the text below. Then delete the word `LINK` (keep the quotation marks) and tap the **Shortcut Input** button above the keyboard.

   ```
   yt-dlp -x --audio-format mp3 --audio-quality 0 --no-playlist -P ~/Documents/Audio/ "LINK"
   ```

6. Tap **Done**.

If you cannot find **Execute Command**, open a-Shell mini once more and search again.

## Use it

1. Open a video in YouTube and tap **Share**.
2. Scroll the lower row of the share sheet and tap **Save Audio**. The first time, tap **More** and switch Save Audio on.
3. Keep a-Shell mini on screen until it finishes. It may open briefly.
4. Open **Files > On My iPhone > a-Shell > Audio**. Your mp3 is there.

## Troubleshooting

| What you see | What to do |
|--------------|------------|
| Save Audio is missing from the share sheet | Open the shortcut, tap **i**, and check **Show in Share Sheet** is on. Then try **More** in the share sheet. |
| Nothing is saved | Open a-Shell mini and wait a few seconds. Downloads run while the app is on screen. |
| Error mentioning 403, or it worked before and now does not | YouTube changed something. Repeat **Install step 2** to get the newest yt-dlp. |
| `command not found` | Repeat **Install step 2**, then fully close and reopen a-Shell mini. |

Still stuck? [Open an issue](../../issues) and include the error text and your iOS version.

## FAQ

**Does it need an internet connection?**
Yes. It downloads the audio from YouTube, and Install step 2 downloads yt-dlp.

**Why a-Shell mini and not the full a-Shell?**
The mini version is about 391 MB and already includes Python and ffmpeg. The full a-Shell is about 2 GB and is not needed.

**Why not an App Store app?**
Apple has historically removed apps that download from YouTube, so a store release is unlikely. A Shortcut plus a terminal app avoids that.

**Why do I build the Shortcut myself?**
Apple only accepts Shortcuts that are signed and shared through iCloud links, which ties them to an Apple account. The manual steps keep this project free of accounts and links.

**Does this collect any data?**
No. This project has no servers, analytics or tracking. Your device talks to YouTube and to GitHub (to fetch yt-dlp), like any other download.

**Is this legal?**
That depends on the video and your country. See the disclaimer below.

## Status

Beta. The full flow (YouTube Share, Save Audio shortcut, a-Shell mini, mp3 in Files) is tested on an iPhone. Reports from other devices and iOS versions are welcome.

## Roadmap

- [x] On-device yt-dlp to mp3 in a-Shell mini
- [x] End-to-end test of the share-sheet Shortcut
- [ ] Self-updating Shortcut that installs and updates yt-dlp on every run
- [ ] Demo recording and screenshots
- [ ] Native iOS app with a share extension, for people who build from source

## Contributing

Bug reports, wording fixes and device test results are all useful. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Disclaimer

This project is for educational purposes. Downloading content from YouTube may violate its Terms of Service and copyright law in your country. Only use it for content you own, content under a licence that permits it (for example Creative Commons or public domain), or where you otherwise have permission. You are responsible for how you use it. The authors accept no liability. This project is not affiliated with YouTube, Google, Apple, yt-dlp or a-Shell.

## Acknowledgements

Built on the work of [yt-dlp](https://github.com/yt-dlp/yt-dlp), [a-Shell](https://github.com/holzschu/a-shell) and [FFmpeg](https://ffmpeg.org/).

## Licence

MIT, see [LICENSE](LICENSE).

---

## For developers

### Optional: self-hosted API

If the on-device setup does not work for you, `server/` contains a small FastAPI service you can run on a machine you control (Raspberry Pi, home Mac, VPS). The Shortcut then sends the link to it and saves the mp3 it returns. Setup is in [docs/ios-shortcut-server.md](docs/ios-shortcut-server.md).

```bash
cp .env.example .env        # set AUDIO_API_TOKEN to a long random value
docker compose up -d --build
```

`GET /audio?url=<youtube url>&format=mp3|m4a` with an `X-API-Token` header returns the audio file. `GET /health` returns `{"status": "ok"}`. Only YouTube links are accepted, playlists are ignored, long videos are rejected, and temporary files are deleted after each response. Always set a token, and put the service behind HTTPS or a private network such as Tailscale before exposing it.

### Development

```bash
cd server
pip install -r requirements-dev.txt
cd .. && pytest
```

More on the on-device setup is in [docs/ios-on-device.md](docs/ios-on-device.md).
