"""Minimal Managed Agents client.

Creates a session against a pre-existing agent, streams its events, and prints
the agent's text as it arrives.

Flow (Managed Agents mandatory flow: agent once -> session every run):
  1. The agent already exists and is referenced by ID -- `model`, `system` and
     `tools` live on the agent object, never on the session.
  2. `sessions.create` starts one run against it inside an environment.
  3. The stream is opened BEFORE the kickoff message is sent, so no early
     events are missed.
  4. The loop ends on a terminal `session.status_idle` or on
     `session.status_terminated`.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python main.py "Summarize what you can do"
"""

from __future__ import annotations

import os
import sys

import anthropic

# The agent and the environment are persistent, pre-created resources.
# Never call agents.create() in the request path.
AGENT_ID = os.environ.get("AGENT_ID", "agent_01B8E49FwYuGuun4XA29oHwa")
ENVIRONMENT_ID = os.environ.get("ENVIRONMENT_ID", "env_01Ct2hoinY78KyxprjeDKGCg")

DEFAULT_PROMPT = "Introduce yourself and describe what you can help with."


def run(prompt: str) -> int:
    # Resolves credentials from ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, or an
    # `ant auth login` profile.
    client = anthropic.Anthropic()

    session = client.beta.sessions.create(
        agent=AGENT_ID,
        environment_id=ENVIRONMENT_ID,
        title="minimal-cli-session",
    )
    print(f"session: {session.id}", file=sys.stderr)

    exit_code = 0

    # Stream-first: the stream only delivers events emitted after it opens, so
    # open it before sending the kickoff message.
    with client.beta.sessions.events.stream(session_id=session.id) as stream:
        client.beta.sessions.events.send(
            session_id=session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        )

        for event in stream:
            if event.type == "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="", flush=True)

            elif event.type == "session.error":
                # e.g. model_overloaded, model_rate_limited, billing, mcp_*
                print(f"\n[session.error] {event.error}", file=sys.stderr)
                exit_code = 1

            elif event.type == "session.status_idle":
                # Idle is transient: the session also idles while it waits on a
                # client-side event. Only a non-`requires_action` stop reason is
                # the end of the run.
                reason = event.stop_reason.type
                if reason == "requires_action":
                    # This minimal client services no custom tools or tool
                    # confirmations, so there is nothing to send back -- stop
                    # instead of waiting forever.
                    print(
                        "\n[idle] session is waiting on a client-side event "
                        "(custom tool result or tool confirmation); this client "
                        "does not handle those.",
                        file=sys.stderr,
                    )
                    exit_code = 1
                    break
                if reason == "retries_exhausted":
                    print("\n[idle] retries exhausted", file=sys.stderr)
                    exit_code = 1
                    break
                print(f"\n[idle] {reason}", file=sys.stderr)
                break

            elif event.type == "session.status_terminated":
                # Terminated covers both normal completion and unrecoverable
                # errors; fetch the session to tell them apart.
                print("\n[terminated]", file=sys.stderr)
                break

    return exit_code


def main() -> int:
    prompt = " ".join(sys.argv[1:]) or DEFAULT_PROMPT
    try:
        return run(prompt)
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        return 130
    except anthropic.NotFoundError as e:  # 404 - unknown agent or environment ID
        print(f"not found: {e.message}", file=sys.stderr)
    except anthropic.AuthenticationError as e:  # 401 - missing or bad credential
        print(f"auth failed: {e.message}", file=sys.stderr)
    except anthropic.RateLimitError as e:  # 429 - retryable
        print(f"rate limited: {e.message}", file=sys.stderr)
    except anthropic.APIStatusError as e:  # any other non-2xx response
        print(f"api error {e.status_code}: {e.message}", file=sys.stderr)
    except anthropic.APIConnectionError as e:  # network failure before a response
        print(f"connection error: {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
