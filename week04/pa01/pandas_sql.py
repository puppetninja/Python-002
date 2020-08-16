#!/usr/bin/env python3
import pandas as pd
import numpy as np

# Generate sample Data and implement 1 to 5
DATA_SIZE = 200
data = pd.DataFrame({
    'id': np.random.randint(1, 3000, DATA_SIZE),
    "age": np.random.randint(1, 80, DATA_SIZE)
     })

print('Pandas equivalent of SQL list:')
print('1. SELECT * FROM data;')
res01 = data
print(res01)

print('2. SELECT * FROM data LIMIT 10;')
res02 = data.head(10)
print(res02)

print('3. SELECT id FROM data;  //id 是 data 表的特定一列')
res03 = data['id']
print(res03)

print('4. SELECT COUNT(id) FROM data')
res04 = data['id'].size
print(res04)

print('5. SELECT * FROM data WHERE id<1000 AND age>30;')
res05 = data[(data['id'] < 1000) & (data['age'] > 30)]
print(res05)

# Generate sample data and implement 6 to 10
DATA_SIZE = 200
table1 = pd.DataFrame({
    'id': np.random.randint(1, 300, DATA_SIZE),
    'order_id': np.random.randint(1, 200, DATA_SIZE)
     })

table2 = pd.DataFrame({
    'id': np.random.randint(1, 300, DATA_SIZE),
    'user_id': np.random.randint(1, 1000, DATA_SIZE)
     })

print('6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;')
res06 = table1.groupby('id').agg({"order_id": pd.Series.nunique})
print(res06)

print('7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;')
res07 = pd.merge(table1, table2, on='id', how='inner')
print(res07)

print('8. SELECT * FROM table1 UNION SELECT * FROM table2;')
res08 = pd.merge(table1, table2, how='outer')
print(res08)

print('9. DELETE FROM table1 WHERE id=10;')
res09 = table1.loc[table1['id'] != 10]
print(res09)

print('10. ALTER TABLE table1 DROP COLUMN column_name;')
column_name = 'id'
res10 = table1.drop(columns=[column_name])
print(res10)
