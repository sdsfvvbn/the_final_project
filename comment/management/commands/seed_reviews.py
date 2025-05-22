from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from comment.models import Review
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = '創建示範用的評價資料'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear_all',
            action='store_true',
            help='在創建新資料前刪除所有現有評價',
        )

    def handle(self, *args, **options):
        self.stdout.write('開始創建評價資料...')
        
        # 處理 clear_all 選項
        if options['clear_all']:
            self.stdout.write('清除所有現有評價...')
            Review.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('評價資料已清除！'))

        # 獲取使用者
        try:
            alan = User.objects.get(username='alan')
            maya = User.objects.get(username='maya')
            alex = User.objects.get(username='alex')
            emily = User.objects.get(username='emily')
            leo = User.objects.get(username='leo')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('請先運行 message 的 seed_data 命令來創建使用者！'))
            return

        # 創建評價
        now = datetime.now()
        
        # 定義評價資料
        reviews_data = [
            # Alan 和 Maya 的互相評價
            {
                'reviewer': alan,
                'rated_user': maya,
                'rating': 5,
                'comment': "隨著我跟maya學鋼琴的時間愈久，每個周末的鋼琴課也成了我生活的另一種日常。即使我周間在上班之餘每天可以練琴的時間，會因為工作是否頻繁出差，而影響每星期可以練琴的總時間。在老師細心專業的教學引導裡，我周間就依老師上課教我的練琴方法，不論練琴時間多或是少，老師總也是能陪我照著我練的狀況，在上課時依我的狀況給我專業的教學。 像這星期，我就因為周間工作的忙碌，能練琴的時間相對少。但是，我還是很喜歡在下班後，練練琴讓自己享受練琴的快樂。我把老師給我的課程進度，不論是徹爾尼56首或是佈爾格彌勒的第一首，我都一小節一小節的慢慢練。上課時，老師就陪著我讓徹爾尼的拍子能一拍一拍的找出拍點，耐心的陪著我練習讓身體感受三拍的節奏，讓自己唱出主旋律的同時，仍繼續身體的律動。當身體、唱歌都捉到感覺了，再到鋼琴上，這種按步就班，一步一步的讓自己意念、視譜和手指都到位，是種愉快的學習經驗。 佈爾格彌勒的第一首，老師照著我這星期的練習進度，陪我讀出樂句，讓我的意念可以引導自己的手指，讓曲子的進行因為樂句的弱強弱的安排，有了音樂的方向。老師引導我，可以從「讓手指彈對音」，漸漸的往「彈出方向」移動。在老師一次又一次耐心的教導下，漸漸的聽見自己也能讓樂句有方向，真的是學琴的快樂。 我想，我很幸運，能遇到好老師。讓我能享受學琴的樂趣。",
                'created_at': now
            },
            {
                'reviewer': maya,
                'rated_user': alan,
                'rating': 5,
                'comment': "呵呵 哈哈 好棒棒",
                'created_at': now + timedelta(minutes=1)
            },
            # Alan 和 Alex 的互相評價
            {
                'reviewer': alan,
                'rated_user': alex,
                'rating': 4,
                'comment': "Alex 的學習能力很強，而且很會舉一反三，是個很好的學習夥伴。",
                'created_at': now + timedelta(minutes=2)
            },
            {
                'reviewer': alex,
                'rated_user': alan,
                'rating': 5,
                'comment': "和alan聊埃及的文化和特殊的體驗非常印象深刻,非常開心！除了增進英文聽力.口語能力.表達力還可以更了解埃及的文化和節日！真的很推薦上課～ 沒想到埃及有AI城市 還有一個和復活節很相像的節日叫做 Sham El Nessim 傳承5000年的埃及節日：迎春日 另外還提到房價 1400萬台幣可在埃及買到5房臥室的villa 但在台灣只能買個公寓吧！ 衝沙體驗 提到騎駱駝第一次很可怕 也會吃駱駝肉喝駱駝奶 我問是等駱駝不能工作才殺來吃嗎 原來工作的駱駝和食用的駱駝不一樣 真的長各種知識 太好玩了",
                'created_at': now + timedelta(minutes=3)
            },
            # Alan 和 Emily 的互相評價
            {
                'reviewer': alan,
                'rated_user': emily,
                'rating': 5,
                'comment': "Emily 的芭蕾舞基礎很紮實，而且她的舞姿優美，是個很好的舞蹈夥伴。",
                'created_at': now + timedelta(minutes=4)
            },
            {
                'reviewer': emily,
                'rated_user': alan,
                'rating': 5,
                'comment': "Alan 的國標舞教學很專業，他會細心指導每個動作的細節，讓我進步很多。",
                'created_at': now + timedelta(minutes=5)
            }
        ]

        # 創建或更新評價
        for review_data in reviews_data:
            review, created = Review.objects.update_or_create(
                reviewer=review_data['reviewer'],
                rated_user=review_data['rated_user'],
                defaults={
                    'rating': review_data['rating'],
                    'comment': review_data['comment'],
                    'created_at': review_data['created_at'],
                    'is_completed': True
                }
            )
            if created:
                self.stdout.write(f'創建了新的評價：{review.reviewer.username} -> {review.rated_user.username}')
            else:
                self.stdout.write(f'更新了現有評價：{review.reviewer.username} -> {review.rated_user.username}')

        self.stdout.write(self.style.SUCCESS(f'已成功處理 {len(reviews_data)} 則評價！')) 