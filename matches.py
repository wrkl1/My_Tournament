# import pandas as pd

# def generate_custom_rounds(teams, group_name):
#     n = len(teams)
#     # خوارزمية الجدولة
#     all_matches = []
#     temp_teams = list(teams)

#     for round_num in range(n - 1):
#         round_matches = []
#         for i in range(n // 2):
#             team1 = temp_teams[i]
#             team2 = temp_teams[n - 1 - i]
#             round_matches.append({
#                 "المجموعة": group_name,
#                 "الجولة": round_num + 1,
#                 "الفريق الأول": team1,
#                 "الفريق الثاني": team2,
#                 "أهداف الأول": "",
#                 "أهداف الثاني": "",
#                 "الحالة": "لم تبدأ"
#             })
#         temp_teams = [temp_teams[0]] + [temp_teams[-1]] + temp_teams[1:-1]
#         all_matches.extend(round_matches)
    
#     return all_matches

# # 1. قائمة الفرق (6 فرق)
# # نصيحة: رتب الفرق هنا بحيث أول مواجهات (1 ضد 6، 2 ضد 5، 3 ضد 4) هي اللي لعبتوها في الجولة الأولى
# group_a_teams = ["شاكر الشمراني", "سلطان القرني", "رمضان العمري", "محمد الشلوي", "شادي محرزي", "انس الغامدي"]
# group_b_teams = ["ماجد الجنيدي", "عماد الزهراني", "حامد درويش", "فهد السهلي", "احمد كش", "عبدالرحمن السلمي"]

# # 2. توليد الجدولة
# matches_a = generate_custom_rounds(group_a_teams, "A")
# matches_b = generate_custom_rounds(group_b_teams, "B")

# # 3. تحويلها لجدول بيانات
# df_matches = pd.DataFrame(matches_a + matches_b)

# # --- هنا السحر: تعديل الجولة الأولى يدوياً لو ما ضبط الترتيب ---
# # تقدر تفتح ملف الإكسل بعد ما يطلع وتعدل أسماء الفرق في "الجولة 1" فقط
# # الكود راح يضمن لك إن الجولات 2، 3، 4، 5 ما فيها تكرار للمباريات

# # 4. حفظ الملف
# with pd.ExcelWriter("Tournament_6_Teams.xlsx") as writer:
#     df_matches.to_excel(writer, sheet_name="جدول المباريات", index=False)
#     # إضافة أوراق الترتيب فارغة
#     pd.DataFrame(columns=["المركز", "الفريق", "نقاط"]).to_excel(writer, sheet_name="ترتيب A", index=False)
#     pd.DataFrame(columns=["المركز", "الفريق", "نقاط"]).to_excel(writer, sheet_name="ترتيب B", index=False)

# print("تم إنشاء الملف لـ 6 فرق. الجولة الأولى موجودة، ويمكنك تعديل أسمائها يدوياً في الإكسل.")