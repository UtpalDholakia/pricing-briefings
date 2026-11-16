# Snapshots

One file per snapshot date, named `YYYY-MM-DD.yml`: the 1st of each month, plus an out-of-cycle file whenever a price change is announced.

Every number in a snapshot is read from the provider's own pricing page on the snapshot date, with `source_checked` set to that date. Never copy last month's file forward without checking, and never edit a past snapshot in place.

The first snapshot is due on **2026-12-01** (Claude's daily run). No snapshot was seeded earlier, because prices could not be verified from provider pages when the database was set up on 2026-11-15.
