# On-device setup (a-Shell mini + Shortcut)

No server needed. A small, free terminal app on your iPhone runs yt-dlp and ffmpeg, and a Shortcut hands it the link from the share sheet.

```
YouTube Share -> Shortcut -> a-Shell mini (yt-dlp + ffmpeg) -> mp3 in Files
```

## 1. Install a-Shell mini

Install **a-Shell mini** from the App Store. It is free, about 391 MB, needs iOS 14 or later, and includes Python and ffmpeg. The full **a-Shell** app is about 2 GB and is not needed here. Open it once.

## 2. Install yt-dlp inside it

Paste this one line into a-Shell and press return:

```bash
mkdir -p ~/Documents/bin ~/Documents/Audio && curl -L -o ~/Documents/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp && chmod +x ~/Documents/bin/yt-dlp
```

It creates `~/Documents/bin` for the tool and `~/Documents/Audio` for your mp3 files. Running it again later updates yt-dlp.

## 3. Test mp3 by hand first

```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 --no-playlist -P ~/Documents/Audio/ "https://www.youtube.com/watch?v=VIDEO_ID"
```

The mp3 appears in the Files app under **On My iPhone > a-Shell > Audio**. If this works, the Shortcut will too.

ffmpeg ships inside a-Shell mini. It has been checked there: ffmpeg 7.0 with the mp3 encoder (`libmp3lame`) enabled. To check your own copy, run `ffmpeg -version` (one dash; `--version` prints the banner and then an error, which is harmless).

## 4. Build the Shortcut

1. Open **Shortcuts**, tap **+**, and name it `Save Audio`.
2. Tap the info button (i), turn on **Show in Share Sheet**, and accept **URLs** only.
3. Add these actions in order:

| # | Action | Settings |
|---|--------|----------|
| 1 | **Get URLs from** | Shortcut Input |
| 2 | **Execute Command** (added by a-Shell) | `yt-dlp -x --audio-format mp3 --audio-quality 0 --no-playlist -P ~/Documents/Audio/ "` then the URL variable from step 1, then `"` |
| 3 | **Show Notification** | `Audio saved` |

4. Tap **Done**.

The **Execute Command** action only appears in Shortcuts after a-Shell (or a-Shell mini) is installed. If it is missing, open a-Shell once and check again.

## 5. Use it

In YouTube tap **Share**, pick **Save Audio**, and wait for the notification. The mp3 lands in **On My iPhone > a-Shell > Audio** in the Files app.

## Limitations

- **Foreground only.** iOS pauses apps in the background, so a-Shell may come to the front while it downloads. Let it finish.
- **403 errors.** YouTube changes often. Re-run the one-line install from step 2 to get the latest yt-dlp.
- **Files stay in a-Shell's folder** and are not synced to iCloud automatically.
- **What is verified.** Tested on an iPhone with a-Shell mini: installing yt-dlp, downloading a video's audio and converting it to mp3 with ffmpeg (`libmp3lame`) all work, and the mp3 plays from Files. Still to be tested end to end: the **Execute Command** action and the share-sheet Shortcut in step 4, which follow a published community guide written for the full a-Shell app. Please report what you see.

## Credit

Based on [this Instructables guide](https://www.instructables.com/Download-YouTube-Videos-or-Extract-MP3s-on-IPhone-/) and the [a-Shell mini App Store listing](https://apps.apple.com/us/app/a-shell-mini/id1543537943).
