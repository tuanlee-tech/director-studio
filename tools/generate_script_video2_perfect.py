#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_script_video2_perfect.py
Tạo kịch bản 157 scenes chuẩn xác 100% cho Video #2 (20 phút = 1.200s, ~36.000 frames).
"""

import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT_DIR / "channels" / "tien-thuc-chien" / "videos" / "lam-phat-loi-song-luong-tang-tien-mat" / "script.md"
BP_PATH = ROOT_DIR / "channels" / "tien-thuc-chien" / "videos" / "lam-phat-loi-song-luong-tang-tien-mat" / "broll-plan.json"

with open(BP_PATH, "r", encoding="utf-8") as f:
    bp_data = json.load(f)

bp_scenes = bp_data.get("scenes", [])

# Danh sách 157 câu thoại narration hoàn chỉnh, trau chuốt, 0 lỗi chính tả
narrations = {
    # --- BEAT 1: HOOK (S001 - S008) ---
    "S001": "Bạn vừa đạt cột mốc mới: được tăng lương từ mười triệu lên hai mươi triệu mỗi tháng.",
    "S002": "Bạn tự hào ăn mừng, cảm thấy những nỗ lực làm việc đã được đền đáp xứng đáng.",
    "S003": "Bạn chuyển sang căn hộ tiện nghi hơn, tin rằng mình sẽ sớm tích lũy được nhiều tiền.",
    "S004": "Thế nhưng cuối tháng, số dư thực tế trong tài khoản vẫn là con số không tròn trĩnh.",
    "S005": "Lương tăng gấp đôi, nhưng cảm giác hoang mang và áp lực chi tiêu vẫn y nguyên.",
    "S006": "Nghịch lý ở chỗ: Khi thu nhập của bạn tăng lên một bậc, thì mức sống và các khoản chi tiêu cũng lập tức tăng theo đúng một bậc tương ứng.",
    "S007": "Trong tài chính cá nhân, đây được gọi là chiếc bẫy lạm phát lối sống, thứ âm thầm triệt tiêu toàn bộ thành quả lao động của người làm công ăn lương.",
    "S008": "Hôm nay, tôi sẽ cùng bạn bóc trần ba chiếc bẫy tâm lý vô hình này và thiết lập hệ thống phòng thủ để giữ lại tiền cho tương lai.",

    # --- BEAT 2: BÓC THỰC TRẠNG 5 KHOẢN NÂNG CẤP VÔ THỨC (S009 - S048) ---
    # Khoản 1: Chỗ ở & Tiện ích (S009 - S016)
    "S009": "Hãy nhìn lại thời điểm bạn vừa tốt nghiệp ra trường, bắt đầu đi làm với mức lương khởi điểm mười triệu đồng mỗi tháng.",
    "S010": "Khi ấy, bạn thuê một căn phòng nhỏ hai triệu rưỡi mỗi tháng, chi tiêu vô cùng tiết kiệm nhưng cuộc sống vẫn hoàn toàn thoải mái và ổn định.",
    "S011": "Nhưng ngay khi nhận quyết định lương hai mươi triệu, ý nghĩ đầu tiên xuất hiện trong đầu bạn là: Mình có tiền rồi, phải chuyển chỗ ở tốt hơn.",
    "S012": "Bạn chuyển sang căn hộ dịch vụ sáu triệu đồng, cộng thêm tiền gửi xe và phí quản lý, mỗi tháng tiêu tốn tới chín triệu đồng cố định.",
    "S013": "Bạn tự thuyết phục bản thân rằng: Ở nơi sang trọng thì mới có tinh thần làm việc tốt hơn và xứng tầm với vị trí công việc mới.",
    "S014": "Thế nhưng bạn không nhận ra rằng: Tiền nhà là khoản chi phí cố định, một khi đã ký hợp đồng thì bạn bắt buộc phải trả đều đặn mỗi tháng.",
    "S015": "Chỉ riêng việc nâng cấp chỗ ở đã âm thầm nuốt chửng hơn bảy mươi triệu đồng tiền chênh lệch lương của bạn trong suốt một năm trời.",
    "S016": "Các chuyên gia tài chính khuyến cáo tiền nhà chỉ nên chiếm tối đa ba mươi phần trăm thu nhập, nhưng bạn đã vô tình vượt ngưỡng an toàn.",

    # Khoản 2: Ăn uống & Cà phê (S017 - S024)
    "S017": "Khoản rò rỉ thứ hai, tinh vi và khó nhận biết hơn rất nhiều, chính là sự thay đổi trong thói quen ăn uống và cà phê hàng ngày của bạn.",
    "S018": "Trước đây bạn hài lòng với cốc cà phê vỉa hè mười lăm nghìn đồng; giờ đây bạn tự động bước vào những chuỗi cà phê thương hiệu sáu mươi lăm nghìn.",
    "S019": "Mỗi ngày chênh lệch năm mươi nghìn đồng nghe có vẻ rất nhỏ bé, nhưng tính tròn một tháng nó đã âm thầm lấy đi thêm một triệu rưỡi.",
    "S020": "Bữa trưa văn phòng từ suất cơm bình dân ba mươi lăm nghìn đồng được nâng cấp lên những bữa ăn tại nhà hàng máy lạnh trên một trăm nghìn đồng.",
    "S021": "Chỉ riêng khoản tiền ăn trưa công sở, bạn đã phải chi thêm gần hai triệu đồng mỗi tháng mà bản thân hoàn toàn không hề cảm thấy xót ruột.",
    "S022": "Vào các dịp cuối tuần, bạn thường xuyên tự thưởng cho mình những bữa lẩu nướng, đồ hải sản đắt tiền với lý do xả hơi sau tuần làm việc vất vả.",
    "S023": "Cộng dồn tất cả lại, tổng chi phí dành cho ăn uống và giải trí hàng tháng của bạn đã tăng vọt từ ba triệu lên tới hơn bảy triệu rưỡi.",
    "S024": "Những khoản chi tiêu nhỏ lẻ này không bao giờ ập đến như một cú sốc lớn, mà ngấm ngầm bào mòn dòng tiền của bạn từng ngày.",

    # Khoản 3: Phương tiện & Di chuyển (S025 - S032)
    "S025": "Hạng mục nâng cấp thứ ba thường xuất hiện khi thu nhập gia tăng chính là phương tiện đi lại và cách thức bạn di chuyển mỗi ngày.",
    "S026": "Bạn bắt đầu có cảm giác chiếc xe máy số cũ kỹ thời sinh viên không còn xứng tầm với mức lương hai mươi triệu và vị trí hiện tại.",
    "S027": "Bạn quyết định tậu ngay một chiếc xe tay ga cao cấp theo hình thức trả góp hai triệu rưỡi mỗi tháng vì đinh ninh mình thừa sức chi trả.",
    "S028": "Vào những hôm thời tiết mưa gió hay nắng gắt, thay vì mặc áo mưa tự lái xe, bạn bắt đầu hình thành phản xạ mở điện thoại đặt taxi công nghệ.",
    "S029": "Bạn tự nhủ rằng sức khỏe và sự tiện nghi là quan trọng, nhưng thực tế mỗi tháng bạn đã tốn thêm một triệu hai trăm nghìn cho các chuyến xe ô tô.",
    "S030": "Chi phí vận hành phương tiện tăng vọt từ năm trăm nghìn đồng trước kia lên mức bốn triệu đồng mỗi tháng, gấp tám lần mức chi tiêu ban đầu.",
    "S031": "Bất kỳ món đồ đắt tiền nào bạn sở hữu cũng đều kéo theo một hệ sinh thái các chi phí phụ trợ đắt đỏ đi cùng để duy trì nó.",
    "S032": "Khi bạn nâng cấp chiếc xe, bạn không đơn thuần chỉ chi tiền mua xe, mà bạn đã tự ký cam kết gánh thêm một chuỗi chi phí định kỳ dài hạn.",

    # Khoản 4: Mua sắm cá nhân & Đồ công nghệ (S033 - S040)
    "S033": "Hạng mục thứ tư là mua sắm cá nhân và đồ công nghệ, nơi chiếc bẫy tâm lý mang tên mình xứng đáng được kích hoạt mạnh mẽ nhất.",
    "S034": "Bạn nâng cấp lên chiếc điện thoại thông minh đời mới nhất ba mươi triệu đồng, sắm thêm đồng hồ thông minh và tai nghe không dây cho đủ bộ.",
    "S035": "Bạn chia nhỏ số tiền lớn đó thành các đợt trả góp lãi suất không phần trăm qua thẻ tín dụng, tự nhủ mỗi tháng chỉ tốn có vài triệu đồng.",
    "S036": "Trong tủ đồ của bạn bắt đầu xuất hiện những chiếc áo sơ mi, đôi giày da hàng hiệu có mức giá đắt gấp ba lần những món đồ ngày trước.",
    "S037": "Bạn mạnh tay mua thẻ tập thể hình cao cấp mười hai triệu đồng một năm, nhưng chỉ sau một tháng đầu tiên bạn hầu như không còn lui tới tập luyện.",
    "S038": "Tính trung bình, các khoản chi tiêu mua sắm ngẫu hứng này đã âm thầm cắn vào ngân sách của bạn thêm ba triệu rưỡi mỗi tháng một cách đều đặn.",
    "S039": "Thói quen lướt sàn thương mại điện tử ban đêm trở thành công cụ giải tỏa áp lực công việc, nhưng nó để lại những đơn hàng không thực sự cần thiết.",
    "S040": "Cảm giác hưng phấn khi đập hộp món đồ mới chỉ kéo dài vài ngày ngắn ngủi, nhưng nghĩa vụ trả nợ sẽ đeo bám bạn suốt sáu tháng đến một năm.",

    # Khoản 5: Chi phí xã giao & Duy trì hình ảnh (S041 - S048)
    "S041": "Khoản chi tiêu cuối cùng trong năm hạng mục nâng cấp vô thức chính là chi phí xã giao, ăn nhậu và duy trì hình ảnh bề ngoài của bản thân.",
    "S042": "Khi đảm nhận vị trí công việc mới, bạn thấy rất khó để chối từ những buổi tiệc sau giờ làm việc hoặc các chuyến đi dã ngoại cuối tuần cùng nhóm.",
    "S043": "Mỗi lần tham gia ăn uống cùng nhóm đồng nghiệp hay đối tác, số tiền chia hóa đơn cho mỗi người chưa bao giờ dưới năm trăm nghìn đến một triệu đồng.",
    "S044": "Tiền mừng cưới hỏi, sinh nhật hay quà biếu đối tác cũng được bạn chủ động nâng mức tiền lên để tương xứng với mức thu nhập hai mươi triệu.",
    "S045": "Khoản ngân sách ngoại giao vô hình này đã tiêu tốn thêm khoảng hai triệu rưỡi mỗi tháng, vượt xa khả năng tích lũy thực tế của bạn.",
    "S046": "Bạn đang phải gồng mình chi trả những khoản tiền đắt đỏ chỉ để gìn giữ một vỏ bọc thành đạt trước ánh nhìn của những người xung quanh.",
    "S047": "Nhìn lại toàn bộ bức tranh: Toàn bộ mười triệu đồng tiền lương tăng thêm đã bị nuốt chửng hoàn toàn bởi năm hạng mục nâng cấp vô thức này.",
    "S048": "Đó chính là câu trả lời vì sao dù lương của bạn có tăng gấp đôi, nhưng ví tiền của bạn vẫn hoàn toàn rỗng không vào mỗi cuối tháng.",

    # --- BEAT 3: SỐ LIỆU & GIẢI PHẪU 3 BẪY TÂM LÝ (S049 - S096) ---
    # Bẫy 1: Cỗ máy thích nghi khoái lạc (S049 - S062)
    "S049": "Vì sao một người có học vấn, thông minh và có thu nhập rất tốt lại dễ dàng rơi vào cái bẫy chi tiêu luẩn quẩn này?",
    "S050": "Nguyên nhân nằm ở một hiện tượng tâm lý học hành vi vô cùng nổi tiếng mang tên cỗ máy thích nghi khoái lạc của con người.",
    "S051": "Bộ não con người có xu hướng thích nghi cực kỳ nhanh chóng trước bất kỳ sự tiện nghi hay điều kiện sung túc vật chất mới nào.",
    "S052": "Khi bạn chuyển từ phòng trọ sang căn hộ chung cư sáu triệu đồng, trong tuần đầu tiên bạn cảm thấy tràn ngập sự hứng khởi và mãn nguyện.",
    "S053": "Nhưng chỉ sau đúng ba mươi ngày sinh sống, căn hộ sang trọng ấy nhanh chóng trở thành tiêu chuẩn hiển nhiên và bình thường mới trong mắt bạn.",
    "S054": "Bạn không còn cảm thấy hạnh phúc hơn trước, nhưng bạn lại tuyệt đối không bao giờ chấp nhận quay về sống ở căn phòng trọ nhỏ ngày xưa.",
    "S055": "Và thế là, bạn lại bắt đầu khao khát một căn hộ cao cấp hơn nữa với giá mười triệu đồng để tìm lại cảm giác hưng phấn ban đầu.",
    "S056": "Hiện tượng này giống như việc chạy trên máy tập: Đôi chân bạn guồng càng nhanh, nhưng vị trí thực tế của bạn thì vẫn dậm chân tại chỗ.",
    "S057": "Bạn buộc phải làm việc nhiều giờ hơn, gánh vác nhiều căng thẳng hơn chỉ để duy trì mức sống xa hoa mà chính mình đã tự tạo ra.",
    "S058": "Đây là chiếc bẫy nguy hiểm nhất: Chúng ta phải đánh đổi tiền bạc tích lũy thật để mua lấy những cảm xúc hưng phấn vô cùng ngắn ngủi.",
    "S059": "Nếu không nhận thức rõ cơ chế này, thì dù lương bạn có chạm mốc năm mươi triệu đồng, bạn vẫn sẽ tiêu sạch năm mươi triệu mỗi tháng.",
    "S060": "Kinh tế học gọi đây là tính bất đối xứng trong tiêu dùng: Nâng mức sống lên chỉ mất một ngày, nhưng hạ xuống thì mất cả năm trời đau đớn.",
    "S061": "Những khoản chi tiêu xa xỉ khi đã trở thành thói quen sẽ bị tâm trí đánh tráo thành những nhu cầu sinh hoạt thiết yếu giả tạo.",
    "S062": "Hiểu rõ và làm chủ được cỗ máy thích nghi này chính là chiếc chìa khóa sống còn giúp bạn chặn đứng đà phá sản thầm lặng của bản thân.",

    # Bẫy 2: Hiệu ứng Đi-đơ-rô (S063 - S076)
    "S063": "Bẫy tâm lý số hai sẽ giải thích vì sao chỉ một món đồ mới mua lại có thể châm ngòi cho cả một chuỗi chi tiêu thảm họa.",
    "S064": "Chiếc bẫy này mang tên Hiệu ứng Đi-đơ-rô, bắt nguồn từ câu chuyện có thật của một triết gia người Pháp vĩ đại vào thế kỷ mười tám.",
    "S065": "Ông sống cả đời thanh đạm và giản dị, cho đến khi bất ngờ được một người bạn quý tặng cho chiếc áo choàng nhung đỏ lộng lẫy.",
    "S066": "Khi khoác chiếc áo choàng lộng lẫy lên người, ông lập tức nhìn căn phòng cũ kỹ của mình với cảm giác kệch cỡm và không tương xứng.",
    "S067": "Để xứng với chiếc áo nhung đỏ, ông quyết định thay chiếc bàn làm việc bằng một chiếc bàn gỗ quý chạm khắc đắt đỏ hơn.",
    "S068": "Có bàn mới, ông lại thấy tấm thảm cũ không hợp, liền mua thêm thảm dệt, tranh treo tường và toàn bộ ghế bọc da sang trọng.",
    "S069": "Kết quả cuối cùng là vị triết gia thông thái đã khánh kiệt toàn bộ tiền bạc chỉ vì muốn hoàn thiện sự đồng bộ cho chiếc áo choàng.",
    "S070": "Trong đời sống hiện đại, khi bạn mua một chiếc điện thoại ba mươi triệu, bạn lập tức muốn mua thêm củ sạc nhanh và tai nghe không dây đắt tiền.",
    "S071": "Từ một chiếc điện thoại ban đầu, bạn bị cuốn vào việc sắm ốp lưng cao cấp, gói bảo hiểm rơi vỡ và đồng hồ thông minh đồng bộ.",
    "S072": "Mua bộ vest mới thì phải sắm đôi giày da hàng hiệu; mua xe tay ga mới thì phải mua thêm mũ bảo hiểm nhập khẩu đắt tiền.",
    "S073": "Mỗi lần mua sắm một món đồ vượt chuẩn, bạn vô tình khởi động một phản ứng dây chuyền chi tiêu phái sinh vô cùng tốn kém.",
    "S074": "Tâm lý muốn mọi thứ xung quanh phải đồng bộ về đẳng cấp chính là thủ phạm khiến tiền bạc của bạn bay màu với tốc độ chóng mặt.",
    "S075": "Để thoát khỏi hiệu ứng này, bạn phải học cách chặt đứt phản ứng dây chuyền ngay từ mắt xích mua sắm đầu tiên một cách dứt khoát.",
    "S076": "Đừng bao giờ mua thêm đồ đạc chỉ để làm cho nó tương xứng với một món đồ xa xỉ khác mà bạn vừa mới sở hữu.",

    # Bẫy 3: Thiên kiến hiện tại & Ảo tưởng tháng sau (S077 - S085)
    "S077": "Bẫy tâm lý số ba là ảo tưởng tai hại nhất: Bạn luôn tự huyễn hoặc bản thân rằng mình sẽ bắt đầu tiết kiệm vào tháng sau.",
    "S078": "Trong kinh tế học hành vi, đây được gọi là Thiên kiến hiện tại: Não bộ luôn ưu tiên sự sung sướng tức thời hơn là lợi ích dài hạn.",
    "S079": "Mỗi khi quẹt thẻ chi tiêu hoang phí, bạn lại tự trấn an: Không sao, tháng sau mình sẽ thắt lưng buộc bụng để bù lại.",
    "S080": "Bộ não có xu hướng xem con người của bạn trong tương lai như một người xa lạ, để mặc người đó gánh chịu mọi hậu quả nợ nần.",
    "S081": "Nhưng khi tháng sau gõ cửa, bạn của hiện tại vẫn tiếp tục tìm ra vô số lý do cấp bách để trì hoãn việc giữ tiền.",
    "S082": "Lời hứa tháng sau mình sẽ tiết kiệm chính là lời nói dối ngọt ngào và nguy hiểm nhất, giam cầm bạn trong cảnh túng thiếu triền miên.",
    "S083": "Nếu bạn đã lặp lại lời hứa này suốt mười hai tháng qua, thì đã đến lúc bạn phải tỉnh ngộ và nhìn thẳng vào sự thật.",
    "S084": "Nguyên tắc thép của tài chính cá nhân: Tiết kiệm không phải việc của tương lai; tiết kiệm là hành động phải thực hiện ngay hôm nay.",
    "S085": "Bây giờ, chúng ta hãy cùng nhau đặt hai kịch bản quản lý mười triệu đồng lương tăng lên bàn cân để thấy rõ sự khác biệt.",

    # Bảng số liệu & Đồ thị phân kỳ (S086 - S096)
    "S086": "Hãy so sánh hai người có cùng mức thu nhập tăng thêm mười triệu: Người A nâng cấp lối sống và Người B trích năm mươi phần trăm đầu tư.",
    "S087": "Người B đem năm triệu mỗi tháng tích sản vào chứng chỉ quỹ với mức sinh lời kỳ vọng mười phần trăm một năm theo lãi kép.",
    "S088": "Sau đúng một năm, người A vẫn có số dư bằng không, trong khi tài khoản của người B đã tích lũy được sáu mươi ba triệu đồng.",
    "S089": "Sáu mươi ba triệu đồng tiền mặt là tấm lá chắn vững chắc, giúp người B an tâm trang trải toàn bộ chi phí sinh hoạt nếu gặp biến cố.",
    "S090": "Sau ba năm, người A bắt đầu kiệt sức vì nợ nần, còn người B đã sở hữu khối tài sản hơn hai trăm mười lăm triệu đồng.",
    "S091": "Sau năm năm kiên trì, người B chính thức cán mốc bốn trăm mười triệu đồng, trong khi người A vẫn dậm chân tại chỗ với hai bàn tay trắng.",
    "S092": "Cảm giác cầm trong tay cuốn sổ tiết kiệm hàng trăm triệu đồng mang lại sự tự do và thanh thản mà không đồ hiệu nào sánh được.",
    "S093": "Sau mười năm, sức mạnh khủng khiếp của lãi kép giúp khối tài sản của người B chính thức vượt ngưỡng một tỷ một trăm triệu đồng.",
    "S094": "Khoảng cách mênh mông giữa con số không tròn trĩnh và một tỷ đồng chính là cái giá vô hình đắt đỏ của sự nuông chiều bản thân.",
    "S095": "Những con số biết nói này là hồi chuông cảnh tỉnh sâu sắc, giúp bạn nhận thức rõ hậu quả khôn lường của việc chi tiêu không kiểm soát.",
    "S096": "Hãy ghi nhớ: Tăng lương không giúp bạn giàu có; chỉ có số tiền bạn thực sự giữ lại và đầu tư mới định hình tương lai của bạn.",

    # --- BEAT 4: TƯƠNG PHẢN (S097 - S116) ---
    "S097": "Để nhìn rõ hơn sự thật này, hãy quan sát hai cuộc đời hoàn toàn trái ngược của chàng trai A bảnh bao và chàng trai B điềm đạm.",
    "S098": "Người A khoác lên mình bộ đồ hiệu đắt tiền, lái chiếc xe tay ga đời mới và luôn xuất hiện với vẻ ngoài hào nhoáng sang chảnh.",
    "S099": "Trong khi đó, người B ăn mặc giản dị, đi chiếc xe máy số quen thuộc và giữ một nếp sống vô cùng mộc mạc, khiêm nhường.",
    "S100": "Nhìn từ bên ngoài, mọi người xung quanh đều nghĩ rằng người A giàu có và thành đạt hơn người B rất nhiều lần.",
    "S101": "Thế nhưng khi biến cố ập đến và công ty cắt giảm nhân sự, người A lập tức rơi vào khủng hoảng hoảng loạn tột độ.",
    "S102": "Tài khoản người A chỉ còn vỏn vẹn sáu triệu đồng, trong khi thẻ tín dụng nợ hai mươi triệu và tiền nhà tháng tới đã đến hạn.",
    "S103": "Ngược lại, người B vẫn thảnh thơi nhâm nhi tách trà, hoàn toàn ung dung trước mọi thông tin biến động của thị trường.",
    "S104": "Người A chỉ có đúng không ngày sinh tồn nếu mất việc, còn người B có đủ tài chính để sống thoải mái suốt hai mươi tư tháng.",
    "S105": "Vì không có tiền dự phòng, người A buộc phải cắn răng chịu đựng áp lực bất công ở công sở mà không dám mở lời phản kháng.",
    "S106": "Còn người B luôn tự tin bảo vệ quan điểm chính đáng của mình, bởi vì anh hoàn toàn có quyền lựa chọn ngẩng cao đầu bước đi.",
    "S107": "Đây là bài học cốt lõi: Đừng bao giờ nhầm lẫn giữa ảo giác giàu có bề ngoài với năng lực tự chủ tài chính thực sự bên trong.",
    "S108": "Hầu hết mọi người chi tiền mua đồ đắt đỏ chỉ vì muốn nhận được sự ngưỡng mộ và công nhận từ những người xung quanh.",
    "S109": "Nhưng nghịch lý là: Người ta không hề ngưỡng mộ bạn, họ chỉ đang mải mê tưởng tượng cảm giác chính họ sở hữu món đồ đó.",
    "S110": "Khi bạn hiểu ra chân lý này, bạn sẽ không còn cảm thấy áp lực phải gồng mình chứng tỏ bản thân bằng những món đồ tiêu sản.",
    "S111": "Sự giàu có thực sự là những thứ vô hình mà mắt thường không thấy được: Là sự tự do, là sự thanh thản và những đêm ngon giấc.",
    "S112": "Trút bỏ được gánh nặng sĩ diện hão huyền chính là bước ngoặt vĩ đại nhất mở ra con đường tự do tài chính cho cuộc đời bạn.",
    "S113": "Lối sống hào nhoáng chỉ mang lại sự kiệt quệ; chỉ có lối sống kỷ luật và biết đủ mới kiến tạo nên sự bình an tự tại lâu dài.",
    "S114": "Đã đến lúc chúng ta dừng ngay việc làm giàu cho người khác và bắt đầu xây dựng hệ thống phòng thủ tài chính kiên cố cho chính mình.",
    "S115": "Ngay sau đây, tôi sẽ trao cho bạn tấm bản đồ hành động với ba tầng phòng thủ vững chắc, đã được hàng nghìn người áp dụng thành công.",
    "S116": "Hãy chuẩn bị sổ tay để ghi chép lại ba nguyên tắc vàng này và áp dụng ngay vào kỳ nhận lương tiếp theo của bạn.",

    # --- BEAT 5: LỘ TRÌNH GIẢI PHÁP (S117 - S149) ---
    # Tầng 1: Đóng băng lối sống 6 tháng (S117 - S126)
    "S117": "Tầng phòng thủ đầu tiên mang tên: Đóng băng mức sống cũ trong ít nhất sáu tháng kể từ ngày bạn nhận quyết định tăng lương.",
    "S118": "Khi nhận quyết định tăng lương, hãy sống như thể mức lương mới vẫn chưa từng xuất hiện trong cuộc sống của bạn.",
    "S119": "Giữ nguyên tiền thuê nhà, giữ nguyên chiếc xe máy hiện tại và giữ nguyên thói quen ăn uống quen thuộc trong đúng một trăm tám mươi ngày.",
    "S120": "Khoảng thời gian đóng băng sáu tháng này giúp bạn có đủ độ lùi tâm lý để bình tĩnh quan sát và xây dựng kế hoạch sử dụng tiền bạc.",
    "S121": "Sáu tháng kỷ luật sẽ giúp bộ não của bạn hạ nhiệt cơn say tăng lương, tìm lại sự điềm tĩnh và tỉnh táo trước mọi cám dỗ phù phiếm.",
    "S122": "Chỉ sau sáu tháng đầu tiên, bạn đã có sẵn sáu mươi triệu đồng tiền mặt tích lũy trong tay để làm một tấm đệm tài chính dự phòng vững chắc.",
    "S123": "Cảm giác có một khoản tiền dự phòng lớn nằm trong tài khoản mang lại cho bạn sự an tâm và tự tin gấp vạn lần những món đồ xa xỉ.",
    "S124": "Đóng băng lối sống hoàn toàn không phải là sự kham khổ, mà là bước chạy đà thông minh để bạn làm chủ hoàn toàn tương lai tài chính.",
    "S125": "Khi đã vượt qua được sáu tháng thử thách đầu tiên, bạn đã chiến thắng tám mươi phần trăm cuộc chiến kiểm soát lòng tham của bản thân.",
    "S126": "Hết sáu tháng đóng băng, bạn hoàn toàn có quyền nâng cấp đời sống, nhưng phải tuân thủ nghiêm ngặt theo công thức phân bổ thông minh tiếp theo.",

    # Tầng 2: Công thức 50/50 & Trả cho mình trước (S127 - S138)
    "S127": "Tầng phòng thủ thứ hai là áp dụng quy tắc chia đôi phần lương tăng thêm theo tỷ lệ năm mươi năm mươi vô cùng khoa học.",
    "S128": "Khi bạn được tăng thêm mười triệu đồng, hãy chia đôi số tiền đó làm hai phần bằng nhau: năm triệu tích sản và năm triệu nâng cấp đời sống.",
    "S129": "Năm mươi phần trăm đầu tiên, tức năm triệu đồng, phải được tự động chuyển ngay vào tài khoản tích sản đầu tư vào đúng ngày nhận lương mỗi tháng.",
    "S130": "Hãy cài đặt lệnh trích tiền tự động định kỳ trên ứng dụng ngân hàng, tiền sẽ được cất đi an toàn trước khi bạn kịp nhìn thấy nó trong ví.",
    "S131": "Đây là nguyên tắc kinh điển: Hãy trả cho bản thân mình trước, coi khoản tích sản này như một khoản thuế tương lai bắt buộc phải nộp.",
    "S132": "Năm mươi phần trăm còn lại, tức năm triệu đồng, bạn được phép thoải mái dùng để nâng cấp chất lượng cuộc sống mà không hề thấy tội lỗi.",
    "S133": "Bạn có thể dùng khoản tiền này để ăn uống ngon hơn, đăng ký các khóa học nâng cao tay nghề hoặc đi du lịch nghỉ dưỡng cùng gia đình.",
    "S134": "Quy tắc này giúp bạn vừa tận hưởng xứng đáng thành quả lao động của mình, vừa không bị ức chế tâm lý do tiết kiệm quá mức cực đoan.",
    "S135": "Bạn tiêu tiền một cách có chủ đích và có hạn mức rõ ràng, vì bạn biết chắc rằng tương lai của mình đã được bảo đảm vững chắc.",
    "S136": "Nhờ công thức này, sau ba năm bạn vừa được tận hưởng cuộc sống chất lượng, vừa tích lũy được hơn hai trăm triệu đồng tài sản thực tế.",
    "S137": "Đó chính là sự cân bằng hoàn hảo giữa việc sống trọn vẹn cho hiện tại và chuẩn bị chu đáo cho sự nghiệp lâu dài trong tương lai.",
    "S138": "Cứ mỗi nấc thang thu nhập mới, tốc độ tích lũy của bạn sẽ tăng gấp đôi, trong khi mức sống vẫn liên tục được nâng cấp đều đặn.",

    # Tầng 3: Ba tài khoản & Bộ lọc 72 giờ (S139 - S149)
    "S139": "Tầng phòng thủ thứ ba là thiết lập hệ thống tự động ba tài khoản ngân hàng riêng biệt kết hợp bộ lọc thời gian bảy mươi hai giờ.",
    "S140": "Đừng bao giờ để chung toàn bộ tiền trong một tài khoản duy nhất; hãy chia tách rạch ròi thành ba dòng tiền với mục đích hoàn toàn độc lập.",
    "S141": "Tài khoản thứ nhất là Tài khoản Sinh hoạt cơ bản: Giữ nguyên mười triệu đồng để trang trải tiền nhà, ăn uống và hóa đơn sinh hoạt định kỳ.",
    "S142": "Tài khoản thứ hai là Két sắt Tích sản: Nhận năm triệu đồng mỗi tháng và gỡ bỏ ứng dụng chuyển tiền trên máy để loại bỏ cám dỗ rút tiêu.",
    "S143": "Tài khoản thứ ba là Tài khoản Trải nghiệm: Dành năm triệu cho mua sắm và giải trí; khi số dư về không, bạn bắt buộc phải dừng chi tiêu.",
    "S144": "Đi kèm với hệ thống ba tài khoản là Bộ lọc bảy mươi hai giờ: Bắt buộc trì hoãn ba ngày trước khi thanh toán món đồ bất kỳ.",
    "S145": "Sau bảy mươi hai giờ suy ngẫm tỉnh táo, hơn tám mươi phần trăm những cơn bốc đồng mua sắm sẽ tự động nguội lạnh và biến mất hoàn toàn.",
    "S146": "Bộ lọc thứ hai là Quy đổi giá trị ra giờ lao động: Đem giá tiền món đồ chia cho mức lương thực tế một giờ làm việc của bạn.",
    "S147": "Với mức lương một trăm nghìn một giờ, chiếc đồng hồ sáu triệu tương đương với sáu mươi giờ lao động miệt mài ngoài công sở của bạn.",
    "S148": "Khi nhìn món đồ dưới góc độ mồ hôi và thời gian sống, bạn sẽ tự khắc đưa ra những quyết định tiêu dùng vô cùng khôn ngoan.",
    "S149": "Ba tầng phòng thủ này kết hợp nhịp nhàng tạo nên bức tường thành kiên cố, bảo vệ trọn vẹn số tiền lương tăng thêm của bạn mãi mãi.",

    # --- BEAT 6: KẾT BÌNH YÊN (S150 - S157) ---
    "S150": "Tài chính cá nhân không phải là cuộc đua phô trương mức sống với thiên hạ, mà là hành trình xây dựng sự bình yên bền vững cho tâm hồn.",
    "S151": "Đó là cảm giác bạn có thể ngủ ngon mỗi đêm, không còn nỗi lo âu thường trực về tiền bạc hay nguy cơ thất nghiệp bất ngờ.",
    "S152": "Sự giàu có thực sự là quyền được tự do lựa chọn công việc mình yêu thích và có toàn quyền kiểm soát quỹ thời gian của bản thân.",
    "S153": "Hãy để mỗi đồng tiền tăng thêm trở thành từng viên gạch vững chắc xây dựng nên sự độc lập và tự do tài chính đích thực của bạn.",
    "S154": "Từ kỳ lương tới, hãy áp dụng công thức phòng thủ để giữ trọn thành quả lao động.",
    "S155": "Bạn xứng đáng có được sự thảnh thơi và an tâm tài chính trong suốt cuộc đời.",
    "S156": "Nếu thấy video này hữu ích, hãy nhấn đăng ký kênh Tiền Thực Chiến và chia sẻ video đến người bạn thân thiết nhất của bạn.",
    "S157": "Tôi là người đồng hành của bạn tại Tiền Thực Chiến. Xin chào và hẹn gặp lại bạn trong những phân tích tài chính tiếp theo."
}

# Kiểm tra đảm bảo đủ 157 scenes
assert len(narrations) == 157, f"Chỉ có {len(narrations)} narrations, thiếu {157 - len(narrations)}!"

lines = [
    "# Script — lam-phat-loi-song-luong-tang-tien-mat",
    "Kênh: Tiền Thực Chiến | Ngôn ngữ: vi | Mục tiêu: 20 phút | TTS: vieneu | Voice: Hải Đăng",
    ""
]

for s in bp_scenes:
    sid = s.get("id") or s.get("scene_id")
    num = int(sid.replace("S", ""))
    beat = s.get("beat", "")
    stype = s.get("type", "")
    concept = s.get("concept", "")
    dur = 6 if stype == "AIV" else 8
    nar = narrations.get(sid, "").strip()

    lines.append(f"## Scene {num:03d}")
    lines.append(f"- Beat: {beat}")
    lines.append(f"- Loại dự kiến: {stype}")
    lines.append(f"- Visual concept: {concept}")
    lines.append(f"- Duration ước tính: {dur}s")
    lines.append(f"- Narration: \"{nar}\"")
    lines.append("")

SCRIPT_PATH.write_text("\n".join(lines), encoding="utf-8")
print(f"🎉 ĐÃ GHI THÀNH CÔNG ĐỦ {len(bp_scenes)} SCENES VÀO {SCRIPT_PATH}!")
