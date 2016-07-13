This is my solution to the **Simple Database Challenge**.

I created a test file early on in the project in order to test it with every meaningfull change, and check that nothing broke.

I think that the solution up to the point of the transactions is quite easy and self-explanatory so I will jump right into how I solved the transactions part.

##TRANSACTIONS SOLUTION:
My first thoughts were to create some kind of **Command history** to reverse it when a rollback happened. But I rapidly discarded this solution as this kind actions cannot really be reversed.

Then I thought about using a **list of states**, without altering the `db_state` until the `COMMIT`. Everytime the user issued the `BEGIN` command, a new object would be added to the list and all the new changes would be stored in that object. If a `ROLLBACK` is issued, the last state is discarded; if a `COMMIT` is issued, all the changes are merged.
This presented the problem that, to get a value, I would need to loop through the list of states until I found a record for that value. This solution would perform poorly with a high number of transactions, so it was also discarded.

A fast improvement to the previous solution could have been to copy all the state of the last transaction into the new one, but that would waste a lot of memory, which is also an important concern in the problem proposition.

Finally, I saw that the best solution would be to create a new object with every `BEGIN`, as before, but to make the **changes directly on the current `db_state`**. If the record was already in the database, I would save it's old value to the newly created object in order to recover it if a `ROLLBACK` was executed. A `COMMIT` would delete all the transaction objects.

##EXECUTION:
The solution has been developed for Python 2.7

To execute it interactively `cd` into the project folder and do:

`python DB.py`

To pass a file of commands to standard input do:

`python DB.py < /path/to/your/file`
