# Contributing

Thanks for helping. This project is small, so the most valuable contributions are usually reports from real devices.

## Ways to help

- **Test on your device.** Follow the README exactly and report what worked and what did not.
- **Improve the wording.** If a step confused you, it will confuse others. Suggest clearer text.
- **Report breakage.** YouTube changes often. If downloads fail, tell us the error.
- **Add fixes and features.** Small, focused pull requests are easiest to review.

## Reporting a bug

Open an issue and include:

- iOS version and device model
- a-Shell mini version (run `version` in a-Shell mini if available)
- yt-dlp version (run `yt-dlp --version`)
- The exact error text, or a screenshot
- What you expected to happen

Please do not paste personal information or private video links.

## Pull requests

1. Fork the repository and create a branch.
2. Keep the change focused on one thing.
3. For wording changes, keep the instructions short and plain. The README is written for people who are not technical.
4. For code in `server/`, run the tests before opening the pull request:
   ```bash
   cd server
   pip install -r requirements-dev.txt
   cd .. && pytest
   ```
5. Describe what you changed and how you tested it.

## Style

- Plain language, short sentences.
- No claims about things that have not been tested. Mark untested steps as untested.
- Do not add tracking, analytics or any service that collects user data.

## Scope

This project is for educational purposes. Contributions that help people infringe copyright, bypass paid content or access private videos will not be accepted.
