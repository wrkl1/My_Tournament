import pandas as pd
import re

def full_update():
    file_path = "Tournament_6_Teams.xlsx"
    html_file = "Schedule.html"
    
    # 1. قراءة البيانات من الإكسل
    try:
        matches_df = pd.read_excel(file_path, sheet_name='Matches')
        # قراءة الفرق (تأكد من أن header=1 صحيح حسب ملفك)
        group_a_teams = pd.read_excel(file_path, sheet_name='Group A', header=1)['Team'].tolist()
        group_b_teams = pd.read_excel(file_path, sheet_name='Group B', header=1)['Team'].tolist()
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return

    # --- دالة حساب ترتيب المجموعات ---
    def get_stats(teams, group_name):
        # [Played, Points, Win, Draw, Lose, Goals For, Goals Against, Diff]
        stats = {team: [0, 0, 0, 0, 0, 0, 0, 0] for team in teams if pd.notna(team)}
        df_g = matches_df[matches_df['Group'] == group_name]
        
        for _, r in df_g.iterrows():
            g1, g2 = r['Goals 1'], r['Goals 2']
            if pd.notna(g1) and pd.notna(g2):
                t1, t2 = r['Team 1'], r['Team 2']
                if t1 in stats and t2 in stats:
                    stats[t1][0]+=1; stats[t2][0]+=1 # Played
                    stats[t1][5]+=g1; stats[t1][6]+=g2 # Goals
                    stats[t2][5]+=g2; stats[t2][6]+=g1
                    if g1 > g2: 
                        stats[t1][1]+=3; stats[t1][2]+=1; stats[t2][4]+=1
                    elif g2 > g1: 
                        stats[t2][1]+=3; stats[t2][2]+=1; stats[t1][4]+=1
                    else: 
                        stats[t1][1]+=1; stats[t2][1]+=1; stats[t1][3]+=1; stats[t2][3]+=1
                    stats[t1][7] = stats[t1][5] - stats[t1][6]
                    stats[t2][7] = stats[t2][5] - stats[t2][6]
        
        df = pd.DataFrame.from_dict(stats, orient='index', columns=['Played', 'Points', 'Win', 'Draw', 'Lose', '+', '-', '=']).reset_index()
        df.columns = ['Team', 'Played', 'Points', 'Win', 'Draw', 'Lose', '+', '-', '=']
        # ترتيب حسب النقاط ثم فرق الأهداف ثم الأهداف المسجلة
        df = df.sort_values(by=['Points', '=', '+'], ascending=False).reset_index(drop=True)
        df.insert(0, 'Rank', range(1, len(df)+1))
        return df

    # --- تحويل ترتيب الفرق إلى أسطر HTML ---
    def df_to_rows(df):
        res = ""
        for _, r in df.iterrows():
            res += f"<tr><td>{int(r['Rank'])}</td><td>{r['Team']}</td><td>{int(r['Played'])}</td><td>{int(r['Points'])}</td><td>{int(r['Win'])}</td><td>{int(r['Draw'])}</td><td>{int(r['Lose'])}</td><td>{int(r['+'])}</td><td>{int(r['-'])}</td><td>{int(r['='])}</td></tr>\n"
        return res

    # --- تجهيز جدول المباريات (Matches Tab) ---
    all_matches_html = ""
    for _, r in matches_df.iterrows():
        round_val = int(r['Round']) if pd.notna(r['Round']) else "-"
        group_val = r['Group'] if pd.notna(r['Group']) else "-"
        t1, t2 = r['Team 1'], r['Team 2']
        g1, g2 = r['Goals 1'], r['Goals 2']
        
        # تحويل الأهداف لنصوص (إذا لم تلعب المباراة نضع شرطة)
        s1 = int(g1) if pd.notna(g1) else "-"
        s2 = int(g2) if pd.notna(g2) else "-"
        
        # تنسيق اللون للنتائج
        score_style = "style='color:#f1c40f; font-weight:bold;'" if pd.notna(g1) else ""
        
        all_matches_html += f"""
        <tr>
            <td>{round_val}</td>
            <td>{group_val}</td>
            <td>{t1}</td>
            <td {score_style}>{s1}</td>
            <td {score_style}>{s2}</td>
            <td>{t2}</td>
        </tr>\n"""

    # --- التحديث الفعلي لملف HTML ---
    try:
        with open(html_file, "r", encoding="utf-8") as f: 
            content = f.read()
        
        # استبدال محتوى الجداول باستخدام id الخاص بكل منهما
        content = re.sub(r'<tbody id="matches-body">.*?</tbody>', f'<tbody id="matches-body">\n{all_matches_html}</tbody>', content, flags=re.DOTALL)
        content = re.sub(r'<tbody id="table-body-a">.*?</tbody>', f'<tbody id="table-body-a">\n{df_to_rows(get_stats(group_a_teams, "A"))}</tbody>', content, flags=re.DOTALL)
        content = re.sub(r'<tbody id="table-body-b">.*?</tbody>', f'<tbody id="table-body-b">\n{df_to_rows(get_stats(group_b_teams, "B"))}</tbody>', content, flags=re.DOTALL)

        with open(html_file, "w", encoding="utf-8") as f: 
            f.write(content)
        print("✅ Success! Schedule, Standings A, and Standings B updated.")
    except Exception as e:
        print(f"❌ Error updating HTML file: {e}")

# تشغيل التحديث
full_update()