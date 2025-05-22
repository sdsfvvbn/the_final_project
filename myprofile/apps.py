from django.apps import AppConfig

#設定 myprofile 這個 Django app 的基本資訊
class MyprofileConfig(AppConfig):
    # 預設主鍵型態為 BigAutoField（自動遞增的大整數）
    default_auto_field = "django.db.models.BigAutoField"
        # 指定這個 app 的名稱（要和資料夾名稱一致）
    name = "myprofile"
