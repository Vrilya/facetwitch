# Twitch-Facebook Chat Bridge

This Python script acts as a bridge between a Twitch chat and a Facebook chat. It works by establishing a connection to a specified Twitch chat using IRC protocol and a Facebook chat using the Facebook Chat API, with the ability to pass messages back and forth.

## How does this script work?

- The script first logs into Facebook using session cookies, and then connects to a Twitch chat channel through IRC (Internet Relay Chat).
- If either the login or connection fails, it retries after 5 seconds.
- When a new message arrives from the connected Facebook user, the script sends that message to the Twitch channel.
- When a new message arrives in the Twitch channel, the script sends that message to the connected Facebook user.
- The script keeps running in an infinite loop until it is manually stopped.

## How to use this script?

### Prerequisites

- Python 3.6 is recommended when using this script as fbchat doesn't work correctly with higher versions.
- The `fbchat` Python package installed in your Python environment. You can install it with the command `pip install fbchat`.

### Steps to run the script

1. Open the script in a text editor.
2. Replace `<fb bot c_user number>`, `<xs string>`, and `<your own fb c_user number>` in the `cookies` and `user_id` variables with your actual Facebook session cookies and user ID.
3. Replace `<channel>`, `<twitch user name>`, and `<oauth>` in the `server`, `channel`, `botnick`, and `password` variables with the actual Twitch IRC server, channel, bot username, and oauth token respectively.
4. Save the script and run it in a Python environment.

### Note
Always remember to keep your session cookies and oauth tokens safe and do not share them with others.

### Shutting down the script

To shut down the script, simply stop the script execution in your Python environment or press Ctrl+C in the terminal.

---

Remember that this README assumes that the reader has a certain amount of knowledge about Python programming, using session cookies, and OAuth tokens. If your users may not have this knowledge, you might want to include additional information or links to tutorials.
