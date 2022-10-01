-
(abbreviate | abreviate | brief) {user.abbreviation}: "{abbreviation}"
(abbreviate | abreviate | brief) {user.abbreviation} over: "{abbreviation}"

<user.formatters> (abbreviate | abreviate | brief) {user.abbreviation}:
    user.insert_formatted(user.abbreviation, user.formatters)
<user.formatters> (abbreviate | abreviate | brief) {user.abbreviation} over:
    user.insert_formatted(user.abbreviation, user.formatters)
