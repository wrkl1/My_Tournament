import pandas as pd

def update_tournament_results(file_path):
    # 1. قراءة البيانات
    try:
        matches_df = pd.read_excel(file_path, sheet_name='Matches')
    except Exception as e:
        print(f"خطأ في قراءة ورقة Matches: {e}")
        return

    # تحويل الأهداف لأرقام
    matches_df['Goals 1'] = pd.to_numeric(matches_df['Goals 1'], errors='coerce')
    matches_df['Goals 2'] = pd.to_numeric(matches_df['Goals 2'], errors='coerce')

    # 2. تجهيز بيانات المجموعات
    group_a_df = pd.read_excel(file_path, sheet_name='Group A', header=1)
    group_b_df = pd.read_excel(file_path, sheet_name='Group B', header=1)

    def calculate_stats(teams_list, matches_filter):
        # [Played, Points, Win, Draw, Lose, +, -, =]
        # لاحظ خليت Played هو الأول (رقم 0) و Points هو الثاني (رقم 1)
        stats = {team: [0, 0, 0, 0, 0, 0, 0, 0] for team in teams_list if pd.notna(team)}
        
        for _, row in matches_filter.iterrows():
            t1, t2 = row['Team 1'], row['Team 2']
            g1, g2 = row['Goals 1'], row['Goals 2']
            
            if pd.notna(g1) and pd.notna(g2):
                stats[t1][0] += 1 # Played t1
                stats[t2][0] += 1 # Played t2
                stats[t1][5] += g1 # +
                stats[t1][6] += g2 # -
                stats[t2][5] += g2 # +
                stats[t2][6] += g1 # -

                if g1 > g2:
                    stats[t1][2] += 1 # Win
                    stats[t1][1] += 3 # Points
                    stats[t2][4] += 1 # Lose
                elif g2 > g1:
                    stats[t2][2] += 1 # Win
                    stats[t2][1] += 3 # Points
                    stats[t1][4] += 1 # Lose
                else:
                    stats[t1][3] += 1 # Draw
                    stats[t2][3] += 1 # Draw
                    stats[t1][1] += 1 # Points
                    stats[t2][1] += 1 # Points
                
                stats[t1][7] = stats[t1][5] - stats[t1][6] # =
                stats[t2][7] = stats[t2][5] - stats[t2][6] # =
        
        # 3. ترتيب الأعمدة الجديد هنا
        cols = ['Played', 'Points', 'Win', 'Draw', 'Lose', '+', '-', '=']
        new_df = pd.DataFrame.from_dict(stats, orient='index', columns=cols).reset_index()
        new_df.columns = ['Team'] + cols
        
        # الترتيب في العرض يبقى على النقاط (Points) ثم الفارق (=)
        new_df = new_df.sort_values(by=['Points', '=', '+'], ascending=False).reset_index(drop=True)
        new_df.insert(0, 'Rank', range(1, len(new_df) + 1))
        return new_df

    # 4. الحساب والحفظ
    final_a = calculate_stats(group_a_df['Team'].tolist(), matches_df[matches_df['Group'] == 'A'])
    final_b = calculate_stats(group_b_df['Team'].tolist(), matches_df[matches_df['Group'] == 'B'])

    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        final_a.to_excel(writer, sheet_name='Group A', index=False, startrow=1)
        final_b.to_excel(writer, sheet_name='Group B', index=False, startrow=1)

    print("✅ تم التحديث! عمود Played الآن يظهر قبل Points.")

update_tournament_results("Tournament_6_Teams.xlsx")