
### Why should we bother with databases at all?

```{index} database; reasons to use
```

Opening a database involved a lot more effort than just opening a `.csv`, or any of the
other plain text or Excel formats. We had to open a connection to the database,
then use `ibis` to translate `pandas`-like
commands (the `[]` operation, `head`, etc.) into SQL queries that the database
understands, and then finally `execute` them. And not all `pandas` commands can currently be translated
via `ibis` into database queries. So you might be wondering: why should we use
databases at all?

Databases are beneficial in a large-scale setting:

- They enable storing large data sets across multiple computers with backups.
- They provide mechanisms for ensuring data integrity and validating input.
- They provide security and data access control.
- They allow multiple users to access data simultaneously
  and remotely without conflicts and errors.
  For example, there are billions of Google searches conducted daily in 2021 {cite:p}`googlesearches`.
  Can you imagine if Google stored all of the data
  from those searches in a single `.csv` file!? Chaos would ensue!

