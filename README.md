# NCRE_III_linux

题库文件`data.dat`来自未来教育`未来教育考试系统V4.0`

运行python decrypt_data.py data.dat output.db得到可读的SQLite数据库`output.db`


##### 查看题目方法：

```
$ sqlite3 output.db
sqlite> .table
sqlite> select *from Jft_Exam;
```
