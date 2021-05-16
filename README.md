# zendesk-redactor

`zendesk-redactor` is a command-line interface for the Zendesk [Ticket
Redaction](https://www.zendesk.com/apps/support/ticket-redaction/) app.

## Motivation

The usability of the Ticket Redaction app is not so good. The redaction form does not support submitting multi-line
input, so if you have multiple text snippets that you need to redact, you'd have to input them into the field and click
the `Redact` button for each of them separately, one-by-one. This is very inefficient and time-consuming.

This tool tries to remedy this usability oversight by allowing you to redact multiple text snippets at once by either
providing them as command-line arguments, or by writing them into a file and supplying the path to this file as a
command-line option.

The tool also allows you to redact attachments, although it is currently not possible to do this selectively - it's
either all of them or none of them.

This tool is not a silver bullet though. If you have many text snippets that you need to redact, picking them out of the
ticket is still a cumbersome manual process. But this tool will at least allow you to redact all of them at once,
instead of clicking `Redact` for each of them separately.

## Installation

It's Python, so make sure you have Python 3 installed, and run:

```
$ pip install zendesk-redactor
```

Although not strictly necessary, you might want to either create a virtualenv or use something like
[pipx](https://github.com/pipxproject/pipx).

## Usage

### Authentication

In order to authenticate to Zendesk API you must provide the organization name, which usually is the subdomain part of
your Zendesk URL before `zendesk.com` (e.g `obscura` for `https://obscura.zendesk.com`), your agent email address, and
an API [token](https://developer.zendesk.com/rest_api/docs/support/introduction#using-a-zendesk-api-token).

These can be provided in two ways.

1. As command-line options:

```
$ redactor --organization obscura --email agent@obscura.com --token BigSecret42
```

2. As environment variables:

```
export ZREDACTOR_ORGANIZATION=obscura
export ZREDACTOR_EMAIL=agent@obscura.com
export ZREDACTOR_TOKEN=BigSecret42
```

### Redacting text snipets

The following command will redact all occurrences of the text snippets `foo`, `bar`, `baz` in the ticket with ID 1742:

```
$ redactor --organization obscura --email agent@obscura.com --token BigSecret42 --ticket-id 1742 snippets foo bar baz
```

Alternatively, if you use environment variables for authentication:

```
$ redactor --ticket-id 1742 snippets foo bar baz
```

The following command will redact all occurrences of the text snippets provided in a file `/tmp/to_redact.txt` in the
ticket with ID 1742:

```
$ redactor --organization obscura --email agent@obscura.com --token BigSecret42 --ticket-id 1742 snippets -f /tmp/to_redact.txt
```

Alternatively, with authentication environment variables set:

```
$ redactor --ticket-id 1742 snippets -f /tmp/to_redact.txt
```

The file must contain one snippet per line.

### Redacting attachments

The following command will redact all attachments in ticket with ID 1742:

```
$ redactor --organization obscura --email agent@obscura.com --token BigSecret42 --ticket-id 1742 attachments
```

Alternatively, with authentication environment variables set:

```
$ redactor --ticket-id 1742 attachments
```

Note that currently it is not possible to redact attachments selectively.
