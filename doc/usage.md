# Usage

## Permissions

Access to resources in Skyportal is controlled in two ways:

- *ACLs* control which actions a user is allowed to perform: create a new user, upload spectra, post comments, etc.
- *Groups* are sets of sources that are accessible to members of that group
    - Members can also be made an *admin* of the group, which gives them group-specific permissions to add new users, etc.
    - The same source source can belong to multiple groups

*Roles* are collections of *ACLs*, and are a convenient way of giving
users the same subset of permissions.

## Adding roles to users

- User permissions can be managed on the `/users/` page (click through from profile)

## Adding users to groups

- Groups membership can be managed on the `/groups/` page (click through from profile)

## Important Makefile targets

Run `make` to get a list of Makefile targets.  Here are some commonly
used ones:

General:

- help : Describe make targets

DB preparation:

- db_init : Create database
- db_clear : Drop and re-create DB

Launching:

- run : Launch the web application
- log : Tail all log files

Testing:

- test : Launch web app & execute frontend tests
- test_headless : (Linux only) The above, but without a visible browser

Development:

- lint : Run ESLint on all files.  Installs ESLint if necessary.
- lint-unix : Same as above, but outputs in a format that most text editors can parse
- lint-githook : Install a Git pre-commit hook that lints staged
                 chunks (this is done automatically when you lint
                 for the first time).
