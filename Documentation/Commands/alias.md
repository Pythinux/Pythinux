# alias
`alias` is an alias manager, which controls the aliases set by your system.
## About Aliases
Aliases are essentially shortcuts for commands. If you have an alias called `?` that you set to the `help` command, typing `?` would run the `help` command.

Note that aliases do not support arguments, so this works:
`cmd --> command`

But this does not:

`cmd -e --> command -e`

Unless you specify `cmd -e` as an alias directly. This may be addressed in a future release, but I do not think that it is a major issue.

Aliases are applied by the `main()` function, so your shell does not need to support them directly. 

## Alias Command Parameters
The `alias` command has several different operations for controlling aliases.
### `alias list`
This command lists all aliases that are registered by the system in the format:

``alias --> command``
### ``alias clear``
This removes all aliases from the system in one go.
### ``alias add`
This command adds an alias to the system.

``alias add <alias> <command>``

Using the above syntax, ``alias add ? help`` would create an alias `?` which redirects to `help`.
### ``alias remove``
This command removes an alias from your system.

``alias remove <alias>``

Using the above formatting, `alias remove ?` would delete the `?` alias.