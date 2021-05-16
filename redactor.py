import sys

import click
import requests


@click.group()
@click.pass_context
@click.option(
    "-o",
    "--organization",
    help=(
        "Zendesk organization name. "
        "Usually the zendesk.com subdomain (obscura in obscura.zendesk.com)"
    ),
    required=True,
    envvar="ZREDACTOR_ORGANIZATION",
)
@click.option(
    "-e",
    "--email",
    help=(
        "A Zendesk agent email address. "
        "Usually the email you use to login to Zendesk as an agent"
    ),
    required=True,
    envvar="ZREDACTOR_EMAIL",
)
@click.option(
    "-t",
    "--token",
    help="Zendesk API token",
    required=True,
    envvar="ZREDACTOR_TOKEN",
)
@click.option("-i", "--ticket-id", help="Zendesk ticket ID", required=True)
@click.option(
    "-r",
    "--dry-run",
    help="Only show what would be done, but do not actually do anything",
    is_flag=True,
)
def redact(ctx, organization, email, token, ticket_id, dry_run):
    ctx.ensure_object(dict)

    ctx.obj[
        "base_url"
    ] = f"https://{organization}.zendesk.com/api/v2/tickets/{ticket_id}/comments"
    ctx.obj["auth"] = f"{email}/token", token
    ctx.obj["dry_run"] = dry_run


@redact.command()
@click.pass_context
@click.argument("snippets", nargs=-1, required=False)
@click.option("-f", "--file", type=click.File("r"), required=False)
def snippets(ctx, snippets, file):
    if not snippets and not file:
        raise click.exceptions.UsageError(
            "Either 'SNIPPETS' argument(s) or '-f' / '--file' option must be specified"
        )

    if snippets and file:
        raise click.exceptions.UsageError(
            "Only one of 'SNIPPETS' argument(s) or '-f' / '--file' option must be specified"
        )

    base_url = ctx.obj["base_url"]
    auth = ctx.obj["auth"]
    dry_run = ctx.obj["dry_run"]

    if file:
        snippets = [s.strip() for s in file.readlines() if s.strip()]

    snippets_found = False
    for s in snippets:
        snippet_found = False
        for c in get_comments(base_url, auth):
            if s in c["body"]:
                snippet_found = True
                snippets_found = True
                print(f"Found snippet '{s}' in comment {c['id']}")
                if dry_run:
                    print("Running dry, skipping")
                else:
                    print("Redacting snippet")
                    handle_resp(
                        requests.put(
                            f"{base_url}/{c['id']}/redact.json",
                            json={"text": s},
                            auth=auth,
                        ),
                        error="Redaction failed",
                    )
        if not snippet_found:
            print(f"Snippet '{s}' not found in ticket")
    if not snippets_found:
        print("None of the provided text snippets were found in the ticket")


@redact.command()
@click.pass_context
def attachments(ctx):
    base_url = ctx.obj["base_url"]
    auth = ctx.obj["auth"]
    dry_run = ctx.obj["dry_run"]

    attachments_found = False
    for c in get_comments(base_url, auth):
        for a in c["attachments"]:
            attachments_found = True
            print(f"Found attachment {a['id']} in comment {c['id']}")
            if dry_run:
                print("Running dry, skipping")
            else:
                print("Redacting attachment")
                handle_resp(
                    requests.put(
                        f"{base_url}/{c['id']}/attachments/{a['id']}/redact.json",
                        auth=auth,
                    ),
                    error="Redaction failed",
                )
    if not attachments_found:
        print("Ticket contains not attachments")


def get_comments(base_url, auth):
    resp = requests.get(base_url, auth=auth)
    handle_resp(resp, "Failed to get ticket comments", fail=True)
    return resp.json().get("comments", [])


def handle_resp(resp, error, fail=False):
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"{error}: {e}")
        if fail:
            sys.exit(1)
