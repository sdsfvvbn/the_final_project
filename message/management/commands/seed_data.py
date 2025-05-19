from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from message.models import Message
from datetime import datetime, timedelta


User = get_user_model()
class Command(BaseCommand):
    help = '創建示範用的假資料，包括使用者和訊息'
    
    def add_arguments(self, parser):
        # 添加命令行參數
        parser.add_argument(
            '--users-only',
            action='store_true',
            help='只創建使用者，不創建訊息',
        )
        parser.add_argument(
            '--clear-all',
            action='store_true',
            help='在創建新資料前刪除所有現有資料',
        )

    def handle(self, *args, **options):
        self.stdout.write('開始創建假資料...')
        
        # 處理 clear-all 選項
        if options['clear_all']:
            self.stdout.write('清除所有現有資料...')
            User.objects.filter(username__in=['alan', 'maya', 'alex', 'emily']).delete()
            Message.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('資料已清除！'))

        # 創建使用者
        if User.objects.filter(username='alan').exists():
            self.stdout.write(self.style.WARNING('用戶已存在，跳過創建用戶步驟'))
            alan = User.objects.get(username='alan')
            maya = User.objects.get_or_create(username='maya', defaults={'password': '1234'})[0]
            alex = User.objects.get_or_create(username='alex', defaults={'password': '1234'})[0]
            emily = User.objects.get_or_create(username='emily', defaults={'password': '1234'})[0]
            leo = User.objects.get_or_create(username='leo', defaults={'password': '1234'})[0]
        else:
            # 創建使用者帳號
            self.stdout.write('創建使用者帳號...')
            alan = User.objects.create_user(username='alan', password='1234')
            maya = User.objects.create_user(username='maya', password='1234')
            alex = User.objects.create_user(username='alex', password='1234')
            emily = User.objects.create_user(username='emily', password='1234')
            leo = User.objects.create_user(username='leo', password='1234')
            self.stdout.write(self.style.SUCCESS('使用者帳號創建成功！'))

        # 如果只創建使用者，就在此退出
        if options['users_only']:
            self.stdout.write(self.style.SUCCESS('已創建使用者，並按指定跳過訊息創建。'))
            return

        # 清除現有訊息
        self.stdout.write('清除現有訊息...')
        Message.objects.all().delete()

        # 設定時間戳
        now = datetime.now()
        
        # 創建基本訊息對話
        self._create_basic_messages(alan, maya, alex, emily, leo, now)
        
        self.stdout.write(self.style.SUCCESS(f'已成功創建 {Message.objects.count()} 則訊息！'))
        
    def _create_basic_messages(self, alan, maya, alex, emily, leo, now):
        """創建基本的對話訊息"""
        # Alan 和 Maya 的對話
        Message.objects.create(sender=alan, receiver=maya, text="Hi Maya, 你有特別想學哪一首歌嗎？", created_at=now)
        Message.objects.create(sender=maya, receiver=alan, text="嗨 Alan，沒有特定哪一首ㄟ 但我喜歡聽搖滾音樂", created_at=now + timedelta(seconds=20))
        Message.objects.create(sender=alan, receiver=maya, text="好的那我朝這方向準備 ， 那你這周哪天有空", created_at=now + timedelta(seconds=40))
        Message.objects.create(sender=maya, receiver=alan, text="好得好的！我大概可以在週三下午有空，你怎麼樣？", created_at=now + timedelta(seconds=60))
        Message.objects.create(sender=alan, receiver=maya, text="好的，那我們約週三下午見！", created_at=now + timedelta(seconds=80))

        # Alan 和 Alex 的對話
        Message.objects.create(sender=alan, receiver=alex, text="Hi Alex, 可以問一下你目前的日文水平", created_at=now + timedelta(minutes=1))
        Message.objects.create(sender=alex, receiver=alan, text="嗨囉!我的程度就是能簡短對話", created_at=now + timedelta(minutes=2))
        Message.objects.create(sender=alan, receiver=alex, text="了解了解，那我們用google meet 線上教學你ok嗎", created_at=now + timedelta(minutes=3))
        Message.objects.create(sender=alex, receiver=alan, text="歐虧啊 那週四晚上如何", created_at=now + timedelta(minutes=4))
        Message.objects.create(sender=alan, receiver=alex, text="可以啊，那週四晚上見！", created_at=now + timedelta(minutes=5))

        # Alan 和 Emily 的對話
        Message.objects.create(sender=alan, receiver=emily, text="Hi Emily, 我擅長的舞蹈是國標舞，但我看你的介紹寫說你想交換的是芭蕾舞", created_at=now + timedelta(minutes=6))
        Message.objects.create(sender=emily, receiver=alan, text="哈哈 我也學過芭蕾舞 但後面覺得國標舞比較有趣 所以我兩種都很精通喔", created_at=now + timedelta(minutes=7))
        Message.objects.create(sender=alan, receiver=emily, text="聽起來不錯！那約在中央舞蹈教室", created_at=now + timedelta(minutes=8))
        Message.objects.create(sender=emily, receiver=alan, text="當然可以，我明天上午有空，如何？", created_at=now + timedelta(minutes=9))
        Message.objects.create(sender=alan, receiver=emily, text="好的，那就明早見！", created_at=now + timedelta(minutes=10))
        
        Message.objects.create(sender=alan, receiver=leo, text="嗨!你好呀", created_at=now + timedelta(minutes=6))
        Message.objects.create(sender=alan, receiver=leo, text="我看到你想學吉他", created_at=now + timedelta(minutes=9))
        Message.objects.create(sender=alan, receiver=leo, text="你是初學者嗎!", created_at=now + timedelta(minutes=14))
        Message.objects.create(sender=leo, receiver=alan, text="你好呀!", created_at=now + timedelta(minutes=18))
        Message.objects.create(sender=leo, receiver=alan, text="我之前學過一段時間，會簡單的和弦", created_at=now + timedelta(minutes=21))
        Message.objects.create(sender=leo, receiver=alan, text="那你呢，你以前有學過爵士鼓嗎", created_at=now + timedelta(minutes=24))
        Message.objects.create(sender=alan, receiver=leo, text="了解了解", created_at=now + timedelta(minutes=25))
        Message.objects.create(sender=alan, receiver=leo, text="沒學過，我是初學者", created_at=now + timedelta(minutes=28))
        Message.objects.create(sender=leo, receiver=alan, text="恩恩", created_at=now + timedelta(minutes=29))
        Message.objects.create(sender=alan, receiver=leo, text="那我們要約甚麼時候", created_at=now + timedelta(minutes=31))
        Message.objects.create(sender=alan, receiver=leo, text="你甚麼時候方便", created_at=now + timedelta(minutes=33))
        
        # 創建未讀訊息
        Message.objects.create(sender=alan, receiver=maya, text="Maya，別忘了我們約定的學習時間！", created_at=now + timedelta(minutes=55), is_read=False)
        Message.objects.create(sender=maya, receiver=alan, text="謝謝提醒，Alan，我會準時的！", created_at=now + timedelta(minutes=55), is_read=False)
        Message.objects.create(sender=alan, receiver=alex, text="Alex，明天時間可以延後30分鐘嗎", created_at=now + timedelta(minutes=55), is_read=False)
        Message.objects.create(sender=alan, receiver=emily, text="Emily，我到教室了喔", created_at=now + timedelta(minutes=55), is_read=False)
        Message.objects.create(sender=leo, receiver=alan, text="後天早上，你覺得呢", created_at=now + timedelta(minutes=55))