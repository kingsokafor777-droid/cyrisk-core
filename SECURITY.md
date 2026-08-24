# Security Policy

## Reporting a vulnerability

Please use GitHub private vulnerability reporting for security defects. Do not include secrets,
customer data, or raw incident material in an issue.

## Supported release line

The latest `0.1.x` source release is supported for security fixes.

## Security boundary

This package is offline and payload-blind. It validates record structure and hashes canonical
content; it does not authenticate users, authorize decisions, protect a live database, or verify
the truth of a supplied evidence reference. Deployers of downstream services own identity, secret
management, access control, encryption, retention, and incident response.
