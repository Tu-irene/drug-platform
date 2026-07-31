import os
from supabase import create_client

# 直接填入您的 Supabase 完整正確網址
supabase_url = "https://lbdipjgtntexhnpybuyd.supabase.co"

# 從 Secret 讀取金鑰
supabase_key = os.environ.get("SUPABASE_KEY")

print(f"🔗 正在連線至: {supabase_url}")

try:
    supabase = create_client(supabase_url, supabase_key)

    test_data = [{
        "country": "台灣",
        "brand_name": "吉利達 (測試)",
        "active_ingredient": "Pembrolizumab",
        "dosage_form": "注射劑",
        "strength": "100mg/4mL",
        "licence_status": "有效",
        "official_url": "https://www.fda.gov.tw"
    }]

    print("📤 正在寫入測試資料到 Supabase...")
    res = supabase.table("drug_approvals").insert(test_data).execute()
    print("🎉【大成功】資料已成功寫入 Supabase 資料庫！")

except Exception as e:
    print(f"❌ 寫入失敗，原因: {e}")
