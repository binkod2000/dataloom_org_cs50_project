import sqlite3

//where rc is an int variable if wondering :/
rc = sqlite3_prepare_v2(dbPointer, "pragma table_info ('your table name goes here')", -1, &stmt, NULL);

if (rc==SQLITE_OK)
{
    //will continue to go down the rows (columns in your table) till there are no more
    while(sqlite3_step(stmt) == SQLITE_ROW)
    {
        sprintf(colName, "%s", sqlite3_column_text(stmt, 1));
        //do something with colName because it contains the column's name
    }
}