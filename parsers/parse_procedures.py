import pandas as pd

# Чтение данных из файла Excel
file_path = 'procedures_raw.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet0')

# Переименуем колонку для удобства, если нужно
df.columns = ['category', 'text', 'link']

# Fill in missing values in 'text' column with values from 'category'
df['text'].fillna(df['category'], inplace=True)

df['category'] = df['category'].apply(lambda x: f'"{x}"')
df['text'] = df['text'].apply(lambda x: f'"{x}"')

# Вывод первых строк DataFrame
print(df.head())

df.to_csv('procedures.csv', index=False)