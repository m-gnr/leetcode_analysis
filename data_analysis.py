import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from wordcloud import WordCloud


df = pd.read_csv("leetcode_scrap.csv")
df['Submissions'] = df['Submissions'].apply(lambda x: float(str(x).replace('M', '')) * 1000000 if 'M' in str(x) else float(str(x).replace('K', '')) * 1000 if 'K' in str(x) else float(x))
df['Accepted'] = df['Accepted'].apply(lambda x: float(str(x).replace('M', '')) * 1000000 if 'M' in str(x) else float(str(x).replace('K', '')) * 1000 if 'K' in str(x) else float(x))
df['Acceptance Rate'] = df['Acceptance Rate'].str.replace('%', '').astype(float)
df['Likes'] = df['Likes'].apply(lambda x: float(str(x).replace('K', '')) * 1000 if 'K' in str(x) else float(x))
df['Comments'] = df['Comments'].apply(lambda x: float(str(x).replace('K', '')) * 1000 if 'K' in str(x) else float(x))
df['Tags'] = df['Tags'].apply(lambda x: x.split(', ') if pd.notna(x) else "")
df['Difficulty Level'] = df['Difficulty Level'].str.strip()

tags = {}
for idx, row in df.iterrows():
    for tag in row["Tags"]:
        if tag in tags:
            tags[tag]['count'] += 1
            tags[tag]['indices'].append(idx) 
        else:
            tags[tag] = {'count': 1, 'indices': [idx]} 


tags_list = []
for tag, data in tags.items():
    tags_list.append({
        "Title": tag,
        "Count": data['count'],
        "Indices": data['indices']
    })

tags_df = pd.DataFrame(tags_list)
tags_df_sorted = tags_df.sort_values(by='Count', ascending=False)
tags_df_sorted.to_csv("tags.csv", index=False)

easy_index = df.loc[df['Difficulty Level'] == "Easy"].index.tolist() # 711 easy questions
medium_index = df.loc[df['Difficulty Level'] == "Medium"].index.tolist() # 1337 medium questions
hard_index = df.loc[df['Difficulty Level'] == "Hard"].index.tolist() # 598 hard questions

def calculate(type: str, tag: str, difficulty: int = 0) -> str:
    """
    Parametreler:
        type (str): Hesaplanacak istatistik türü. 
            Geçerli türler: 
                mode
                std
                median
                average
                varians
        
        tag (str): Hesaplamanın yapılacağı alan.
            Seçenekler: 
                Submissions
                Accepted
                Acceptance Rate
                Likes
                Comments

        difficulty (int): Zorluk seviyesi.
            difficulty (int): Hesaplanacak türün zorluk seviyesi.\n
                0 - Tümü
                1 - Kolay 
                2 - Orta
                3 - Zor

        Dönüş Değeri:
        str: Belirtilen zorluk seviyesindeki soruların belirtilen istatistiksel değeri.
    """
    if difficulty not in [0, 1, 2, 3]:
        raise ValueError("Zorluk seviyesi 0, 1, 2 veya 3 olmalıdır.")
    if tag not in ['Submissions', 'Accepted', 'Acceptance Rate', 'Likes', 'Comments']:
        raise KeyError(f"{tag} geçerli bir tag değil. Geçerli seçenekler: 'Submissions', 'Accepted', 'Acceptance Rate', 'Likes', 'Comments'.")
    if type not in ['mode', 'std', 'median', 'average', 'varians']:
        raise KeyError(f"{type} geçerli bir tür değil. Geçerli seçenekler: 'mode', 'std', 'median', 'average', 'varians'.")


    if difficulty == 0:
        indices = df.index
    elif difficulty == 1:
        indices = easy_index
    elif difficulty == 2:
        indices = medium_index
    elif difficulty == 3:
        indices = hard_index

    filtered_data = df.loc[indices, tag]

    if type == "average":
        value = filtered_data.mean()
        return "{:.2f}".format(value)

    elif type == "mode":
        value = filtered_data.mode().iloc[0]
        return str(value)
    
    elif type == "std":
        value = filtered_data.std()
        return "{:.2f}".format(value)
    
    elif type == "median":
        value = filtered_data.median()
        return "{:.2f}".format(value)
    
    elif type == "varians":
        value = filtered_data.var()
        return "{:.2f}".format(value)

def calc_correlation(tag1: str, tag2: str) -> str:
    """
    Belirli iki başlık arasında korelasyon katsayısını hesaplar.

    Parametreler:
    tag1 (str): Korelasyonun hesaplanacağı ilk sütun.
    tag2 (str): Korelasyonun hesaplanacağı ikinci sütun.

    Dönüş Değeri:
    str: İki sütun arasındaki korelasyon katsayısı.
    """
    if tag1 in df.columns and tag2 in df.columns:
        correlation = df[tag1].corr(df[tag2])
        return "{:.2f}".format(correlation)
    else:
        raise KeyError(f"{tag1} veya {tag2} geçerli bir sütun değil.")

def display():
    # Histogram tabloda görselleştirme
    sns.histplot(data=df, x='Likes', hue='Difficulty Level', bins=10, kde=False,
                    palette=['lightpink', 'blue', 'purple'])
    plt.title('Chart of Accepted Submissions')
    plt.xlabel('Number of Accepted Submissions')
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()

    # KDE tabloda görselleştirme
    sns.kdeplot(data=df, x='Accepted', hue='Difficulty Level', common_norm=False)
    plt.title('Density Chart of Accepted Submissions by Difficulty Level')
    plt.xlabel('Number of Accepted Submissions') 
    plt.ylabel('Density')                         
    plt.grid(True)
    plt.show()

    sns.scatterplot(data=df, x='Accepted', y='Submissions', hue='Difficulty Level')
    plt.title('Chart of Accepted Submissions')
    plt.xlabel('Number of Accepted Submissions')  
    plt.ylabel('Number of Submissions')           
    plt.grid(True)                                
    plt.show()

    sns.barplot(data=df, x='Difficulty Level', y='Likes', hue='Difficulty Level', palette=['lightpink', 'blue', 'purple'])
    plt.title('Likes by Difficulty Level')
    plt.xlabel('Difficulty Level')
    plt.ylabel('Average Likes')
    plt.grid(True)
    plt.show()


    # Zorluk seviyesi dağılımını hesaplayalım
    difficulty_counts = df['Difficulty Level'].value_counts()

    # Pasta grafiği
    plt.figure(figsize=(8, 8))
    plt.pie(difficulty_counts, labels=difficulty_counts.index, autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'lightblue', 'lightcoral'])
    plt.title('Difficulty Level Distribution')
    plt.show()

    # Zorluk seviyesine göre başarı oranlarını hesaplayalım
    acceptance_rate_by_difficulty = df.groupby('Difficulty Level')['Acceptance Rate'].mean()

    # Tabloyu yazdırma
    acceptance_rate_table = pd.DataFrame(acceptance_rate_by_difficulty).reset_index()
    acceptance_rate_table.columns = ['Difficulty Level', 'Average Acceptance Rate']
    print(acceptance_rate_table)

    # Zorluk seviyesine göre ortalama başarı oranını hesaplayalım
    acceptance_rate_by_difficulty = df.groupby('Difficulty Level')['Acceptance Rate'].mean()

    # Pasta grafiği oluşturma
    plt.figure(figsize=(8, 6))
    plt.pie(
        acceptance_rate_by_difficulty, 
        labels=acceptance_rate_by_difficulty.index, 
        autopct='%1.1f%%',  # Her dilimde yüzdesini gösterir
        startangle=140,      # Grafiği döndürür
        colors=['lightgreen', 'lightskyblue', 'salmon']
    )
    plt.title('Acceptance Rate by Difficulty Level')
    plt.show()

    sns.scatterplot(data=df, x='Acceptance Rate', y='Likes', hue='Difficulty Level', palette=['green', 'orange', 'red'])
    plt.title('Acceptance Rate vs Likes by Difficulty Level')
    plt.xlabel('Acceptance Rate')
    plt.ylabel('Likes')
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Accepted', y='Submissions', hue='Difficulty Level', bins=30, palette=['lightgreen', 'skyblue', 'coral'])
    plt.title('Accepted vs Submissions by Difficulty Level')
    plt.xlabel('Accepted Submissions')
    plt.ylabel('Total Submissions')
    plt.grid(True)
    plt.show()

    sns.boxplot(data=df, x='Difficulty Level', y='Likes', palette=['lightgreen', 'skyblue', 'salmon'])
    plt.title('Likes Distribution by Difficulty Level')
    plt.xlabel('Difficulty Level')
    plt.ylabel('Likes')
    plt.grid(True)
    plt.show()

    correlation_matrix = df[['Submissions', 'Accepted', 'Acceptance Rate', 'Likes', 'Comments']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='YlGnBu', fmt='.2f')
    plt.title('Correlation Matrix')
    plt.show()

    top_tags = tags_df_sorted.head(10)  # En popüler ilk 10 etiketi al
    sns.barplot(data=top_tags, x='Count', y='Title', palette='viridis')
    plt.title('Top 10 Most Popular Tags by Submissions')
    plt.xlabel('Number of Submissions')
    plt.ylabel('Tag')
    plt.grid(True)
    plt.show()

    tag_counts_by_difficulty = {
        tag: [
            len(df.loc[(df['Difficulty Level'] == 'Easy') & (df['Tags'].apply(lambda tags: tag in tags))]),
            len(df.loc[(df['Difficulty Level'] == 'Medium') & (df['Tags'].apply(lambda tags: tag in tags))]),
            len(df.loc[(df['Difficulty Level'] == 'Hard') & (df['Tags'].apply(lambda tags: tag in tags))])
        ]
        for tag in tags_df_sorted['Title'].head(10)
    }
    tag_counts_df = pd.DataFrame(tag_counts_by_difficulty, index=['Easy', 'Medium', 'Hard']).T
    plt.figure(figsize=(12, 8))
    sns.heatmap(tag_counts_df, annot=True, cmap='Blues', fmt='d')
    plt.title('Tag Popularity by Difficulty Level')
    plt.xlabel('Difficulty Level')
    plt.ylabel('Tags')
    plt.show()


    for level in ['Easy', 'Medium', 'Hard']:
        tags_for_level = ' '.join(
            [tag for tags in df[df['Difficulty Level'] == level]['Tags'] for tag in tags]
        )
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(tags_for_level)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Tag Word Cloud for {level} Level')
        plt.show()

    top_tags = tags_df_sorted['Title'].head(10)
    submissions_by_tag_and_difficulty = {
        tag: [
            df[(df['Tags'].apply(lambda tags: tag in tags)) & (df['Difficulty Level'] == 'Easy')]['Submissions'].sum(),
            df[(df['Tags'].apply(lambda tags: tag in tags)) & (df['Difficulty Level'] == 'Medium')]['Submissions'].sum(),
            df[(df['Tags'].apply(lambda tags: tag in tags)) & (df['Difficulty Level'] == 'Hard')]['Submissions'].sum()
        ]
        for tag in top_tags
    }

    submissions_df = pd.DataFrame(submissions_by_tag_and_difficulty, index=['Easy', 'Medium', 'Hard']).T
    submissions_df.plot(kind='bar', stacked=True, color=['lightgreen', 'lightblue', 'salmon'], figsize=(12, 8))
    plt.title('Submissions by Tag and Difficulty Level')
    plt.xlabel('Tags')
    plt.ylabel('Submissions')
    plt.legend(title='Difficulty Level')
    plt.grid()
    plt.show()

    df['Proportion'] = df['Accepted'] / df['Submissions']
    sns.boxplot(data=df, x='Difficulty Level', y='Proportion', palette=['green', 'orange', 'red'])
    plt.title('Accepted Proportion by Difficulty Level')
    plt.show()
    


display()

  