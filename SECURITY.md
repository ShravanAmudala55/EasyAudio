# Security

## Reporting a vulnerability

If you find a security problem, please report it privately using GitHub's **Report a vulnerability** option on the Security tab of this repository, rather than opening a public issue.

## Scope

- The on-device setup runs commands on your own phone only. It has no server component.
- The optional API in `server/` accepts only YouTube links, requires a token, and deletes temporary files after each request. If you run it, always set `AUDIO_API_TOKEN` and put it behind HTTPS or a private network.
