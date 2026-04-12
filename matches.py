import pandas as pd

teams = [
    "شاكر الشمراني", "رمضان العمري", "ماجد الجنيدي", "حسن محرزي",
    "شادي محرزي", "عماد الزهراني", "انس الغامدي", "حامد درويش",
    "محمد الشلوي", "عبدالرحمن السلمي", "محمود عبده", "احمد كش"
]

n = len(teams)
schedule_data = []
match_number = 1

for round_num in range(1, n):
    for i in range(n // 2):
        home = teams[i]
        away = teams[n - 1 - i]
        
        schedule_data.append({
            "الجولة": f"الجولة {round_num}",
            "رقم المباراة": match_number,
            "الفريق الأول": home,
            "الفريق الثاني": away,
            "أهداف الأول": 0,
            "أهداف الثاني": 0,
            "حالة المباراة": "لم تبدأ"
        })
        match_number += 1
            
    teams = [teams[0]] + [teams[-1]] + teams[1:-1]

# تحويل البيانات لجدول وحفظها
df_schedule = pd.DataFrame(schedule_data)
df_schedule.to_excel("matches_schedule.xlsx", index=False)

print("تم إنشاء جدول الجولات بنجاح! 🏆 افتح ملف matches_schedule.xlsx وشوف الترتيب.")