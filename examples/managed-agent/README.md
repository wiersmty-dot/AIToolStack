# Minimal Managed Agents client

A single-file Python app that talks to an Anthropic Managed Agent: it creates a
session, streams the session's events, and prints the agent's text as it
arrives.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

Credentials also resolve from `ANTHROPIC_AUTH_TOKEN` or an `ant auth login`
profile, so an explicit key is not required if one of those is already set.

## Run

```bash
python main.py "Summarize what you can do"
```

Without an argument it sends a default introduction prompt. Agent text goes to
stdout; session ID and status lines go to stderr, so you can pipe just the
answer:

```bash
python main.py "..." 2>/dev/null
```

## Configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `ANTHROPIC_API_KEY` | — | API credential |
| `AGENT_ID` | `agent_01B8E49FwYuGuun4XA29oHwa` | Pre-created agent to run |
| `ENVIRONMENT_ID` | `env_01Ct2hoinY78KyxprjeDKGCg` | Environment the session runs in |

## How it works

1. **The agent already exists.** Managed Agents separates the persisted,
   versioned agent config from the per-run session: `model`, `system` and
   `tools` live on the agent, and the session only takes a pointer to it. This
   app never calls `agents.create` — it references the agent by ID.
2. **`sessions.create`** starts one run, pinned to the agent's latest version.
3. **Stream first, then send.** `sessions.events.stream` is opened before
   `sessions.events.send` posts the `user.message` event, because the stream
   only delivers events emitted after it opens.
4. **`agent.message`** events carry the agent's output; their text blocks are
   printed as they stream in.
5. **Finishing.** The loop breaks on `session.status_terminated`, or on
   `session.status_idle` with a terminal `stop_reason`. It does *not* break on
   every idle — a session also idles transiently while it waits on the client.

## Scope

This is a kickoff-and-read client, deliberately minimal:

- It does not service custom tools or tool confirmations. If the session idles
  with `stop_reason: requires_action`, the app reports that and exits non-zero
  rather than hanging.
- It does not reconnect a dropped stream. A production client should overlap a
  reconnect with `sessions.events.list` and dedupe by event ID, since the SSE
  stream has no replay.
- It does not archive the session afterwards.

## Errors

SDK exceptions are caught most-specific-first (404, 401, 429, other non-2xx,
then network). `session.error` events on the stream are written to stderr and
set a non-zero exit code. Exit codes: `0` success, `1` error, `130` Ctrl-C.
