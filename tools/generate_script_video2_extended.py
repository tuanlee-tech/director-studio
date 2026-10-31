#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_script_video2_extended.py
Tạo kịch bản 157 scenes cho Video #2 với dung lượng thoại chuẩn xác ~20 phút:
- 7 AIV scenes: 16-18 từ (đảm bảo <= 18 từ cho clip 6.0s).
- 150 GFX/IMG scenes: 21-25 từ (đảm bảo giọng đọc tự nhiên ~7.5s/cảnh).
- Tổng thời lượng giọng đọc: ~1.160s - 1.180s (~19.5 phút).
- Ghép visual cushion 0.3s -> Tổng video đúng chuẩn 20 phút (1.200s, ~36.000 frames).
- 100% chuẩn tiếng Việt miền Bắc: 'nghìn' (thay cho 'ngàn'), 0 từ lóng, 0 tiếng Anh chưa bản địa hóa.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT_DIR / "channels" / "tien-thuc-chien" / "videos" / "lam-phat-loi-song-luong-tang-tien-mat" / "script.md"

scenes = []

def add_s(beat, stype, concept, dur, nar):
    scenes.append({
        'num': len(scenes) + 1,
        'beat': beat,
        'type': stype,
        'concept': concept,
        'dur': dur,
        'nar': nar.strip()
    })

# =========================================================================
# BEAT 1: HOOK (Scenes 001 - 008, 8 scenes, ~60s)
# =========================================================================
add_s('Hook', 'AIV', 'Chàng trai văn phòng 27 tuổi mặc sơ mi trắng mỉm cười hạnh phúc khi nhận thông báo thăng chức và tăng lương gấp đôi lên hai mươi triệu đồng', 6, 'Bạn vừa đạt cột mốc đáng nhớ: được tăng lương từ mười triệu lên hai mươi triệu đồng mỗi tháng.')
add_s('Hook', 'AIV', 'Chàng trai cùng nhóm bạn đồng nghiệp nâng ly cocktail ăn mừng tưng bừng tại quầy bar nhà hàng sang trọng giữa ánh đèn lung linh', 6, 'Bạn tự hào ăn mừng, cảm thấy bao nỗ lực làm việc vất vả cuối cùng đã được đền đáp xứng đáng.')
add_s('Hook', 'AIV', 'Chàng trai đứng giữa căn hộ chung cư mới thuê rộng rãi, ban công ngắm nhìn toàn cảnh thành phố lung linh về đêm', 6, 'Bạn chuyển sang căn hộ tiện nghi hơn, tin chắc rằng mình sẽ sớm tích lũy được nhiều tiền tiết kiệm.')
add_s('Hook', 'AIV', 'Chàng trai thẫn thờ nhìn chằm chằm vào màn hình điện thoại vào ngày hai mươi tám cuối tháng, thông báo số dư tài khoản chỉ còn vài chục nghìn đồng', 6, 'Thế nhưng cuối tháng mở tài khoản, số dư thực tế trong thẻ vẫn là con số không tròn trĩnh đến khó tin.')
add_s('Hook', 'AIV', 'Chàng trai ngồi một mình bên bàn làm việc ban đêm, xoa thái dương trĩu nặng âu lo, tự hỏi tiền của mình đã biến đi đâu', 6, 'Lương tăng gấp đôi, nhưng cảm giác hoang mang và áp lực chi tiêu cuối tháng vẫn y nguyên như trước.')
add_s('Hook', 'GFX', 'Đồ thị đường thẳng song song: Đường lương màu xanh tăng 100% chạy song song với đường chi tiêu màu đỏ tăng 100%', 8, 'Nghịch lý ở chỗ: Khi thu nhập của bạn tăng lên một bậc, thì mức sống và các khoản chi tiêu cũng lập tức tăng theo đúng một bậc tương ứng.')
add_s('Hook', 'GFX', 'Mô hình biểu tượng chiếc bẫy chuột bằng vàng phát sáng mang tên Lạm phát lối sống', 8, 'Trong tài chính cá nhân, đây được gọi là chiếc bẫy lạm phát lối sống, thứ âm thầm triệt tiêu toàn bộ thành quả lao động của người làm công ăn lương.')
add_s('Hook', 'IMG', 'Nam MC đại diện kênh Tiền Thực Chiến mặc sơ mi trắng đeo thẻ bước vào khung hình với vẻ mặt kiên định, sẵn sàng phân tích', 8, 'Hôm nay, tôi sẽ cùng bạn bóc trần ba chiếc bẫy tâm lý vô hình này và thiết lập hệ thống phòng thủ để giữ lại tiền cho tương lai.')

# =========================================================================
# BEAT 2: BÓC THỰC TRẠNG 5 KHOẢN NÂNG CẤP VÔ THỨC (Scenes 009 - 048, 40 scenes)
# =========================================================================
# --- Khoản 1: Chỗ ở & Tiện ích cố định (Scenes 009 - 016) ---
add_s('Bóc thực trạng', 'IMG', 'Hình ảnh căn phòng trọ nhỏ đơn sơ nhưng ấm cúng của những ngày đầu mới đi làm', 8, 'Hãy nhìn lại thời điểm bạn vừa tốt nghiệp ra trường, bắt đầu đi làm với mức lương khởi điểm mười triệu đồng mỗi tháng.')
add_s('Bóc thực trạng', 'GFX', 'Bảng kê chi tiêu cũ: Tiền thuê trọ hai triệu rưỡi, điện nước năm trăm nghìn, tổng cộng ba triệu mỗi tháng', 8, 'Khi ấy, bạn thuê một căn phòng nhỏ hai triệu rưỡi mỗi tháng, chi tiêu vô cùng tiết kiệm nhưng cuộc sống vẫn hoàn toàn thoải mái và ổn định.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật đứng ngắm tòa nhà chung cư mini hiện đại có thang máy và bảo vệ túc trực', 8, 'Nhưng ngay khi nhận quyết định lương hai mươi triệu, ý nghĩ đầu tiên xuất hiện trong đầu bạn là: Mình có tiền rồi, phải chuyển chỗ ở tốt hơn.')
add_s('Bóc thực trạng', 'GFX', 'Hợp đồng thuê nhà mới: Tiền thuê sáu triệu, phí dịch vụ một triệu, điện nước giá thương mại, tổng chín triệu', 8, 'Bạn chuyển sang căn hộ dịch vụ sáu triệu đồng, cộng thêm tiền gửi xe và phí quản lý, mỗi tháng tiêu tốn tới chín triệu đồng cố định.')
add_s('Bóc thực trạng', 'GFX', 'Biểu đồ cán cân: Chi phí nhà ở tăng vọt gấp 3 lần từ 3 triệu lên 9 triệu đồng mỗi tháng', 8, 'Bạn tự thuyết phục bản thân rằng: Ở nơi sang trọng thì mới có tinh thần làm việc tốt hơn và xứng tầm với vị trí công việc mới.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật ngồi trên chiếc ghế sofa mới đắt tiền trong căn hộ, xung quanh là hóa đơn tiền nhà và phí quản lý', 8, 'Thế nhưng bạn không nhận ra rằng: Tiền nhà là khoản chi phí cố định, một khi đã ký hợp đồng thì bạn bắt buộc phải trả đều đặn mỗi tháng.')
add_s('Bóc thực trạng', 'GFX', 'Cột mốc thời gian: Mười tháng thuê nhà mới tiêu tốn chín mươi triệu đồng, tương đương gần một năm tiền lương cũ', 8, 'Chỉ riêng việc nâng cấp chỗ ở đã âm thầm nuốt chửng hơn bảy mươi triệu đồng tiền chênh lệch lương của bạn trong suốt một năm trời.')
add_s('Bóc thực trạng', 'GFX', 'Thước đo ngân sách: Tỷ trọng tiền thuê nhà chiếm tới 45% tổng thu nhập hàng tháng, mức báo động đỏ', 8, 'Các chuyên gia tài chính khuyến cáo tiền nhà chỉ nên chiếm tối đa ba mươi phần trăm thu nhập, nhưng bạn đã vô tình vượt ngưỡng an toàn.')

# --- Khoản 2: Ăn uống & Cà phê hàng ngày (Scenes 017 - 024) ---
add_s('Bóc thực trạng', 'IMG', 'Quán cà phê vỉa hè mộc mạc quen thuộc với cốc cà phê đen đá mười lăm nghìn đồng', 8, 'Khoản rò rỉ thứ hai, tinh vi và khó nhận biết hơn rất nhiều, chính là sự thay đổi trong thói quen ăn uống và cà phê hàng ngày của bạn.')
add_s('Bóc thực trạng', 'IMG', 'Cốc cà phê thương hiệu cao cấp đặt trên bàn làm việc sang trọng có giá sáu mươi lăm nghìn đồng', 8, 'Trước đây bạn hài lòng với cốc cà phê vỉa hè mười lăm nghìn đồng; giờ đây bạn tự động bước vào những chuỗi cà phê thương hiệu sáu mươi lăm nghìn.')
add_s('Bóc thực trạng', 'GFX', 'Phép tính nhân: Chênh lệch năm mươi nghìn mỗi ngày, một tháng ba mươi ngày tiêu tốn thêm một triệu rưỡi tiền cà phê', 8, 'Mỗi ngày chênh lệch năm mươi nghìn đồng nghe có vẻ rất nhỏ bé, nhưng tính tròn một tháng nó đã âm thầm lấy đi thêm một triệu rưỡi.')
add_s('Bóc thực trạng', 'IMG', 'Bàn ăn trưa tại nhà hàng cùng đồng nghiệp trong văn phòng, hóa đơn thanh toán trên một trăm nghìn', 8, 'Bữa trưa văn phòng từ suất cơm bình dân ba mươi lăm nghìn đồng được nâng cấp lên những bữa ăn tại nhà hàng máy lạnh trên một trăm nghìn đồng.')
add_s('Bóc thực trạng', 'GFX', 'Biểu đồ so sánh chi phí ăn trưa: Cơm bình dân 900 nghìn mỗi tháng vs Nhà hàng 2.5 triệu mỗi tháng', 8, 'Chỉ riêng khoản tiền ăn trưa công sở, bạn đã phải chi thêm gần hai triệu đồng mỗi tháng mà bản thân hoàn toàn không hề cảm thấy xót ruột.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật quét mã thanh toán hóa đơn bữa tối thịnh soạn tại nhà hàng lẩu nướng cùng bạn bè', 8, 'Vào các dịp cuối tuần, bạn thường xuyên tự thưởng cho mình những bữa lẩu nướng, đồ hải sản đắt tiền với lý do xả hơi sau tuần làm việc vất vả.')
add_s('Bóc thực trạng', 'GFX', 'Biểu đồ rò rỉ dòng tiền: Tổng chi phí ăn uống giải trí tăng vọt từ 3 triệu lên 7.5 triệu đồng mỗi tháng', 8, 'Cộng dồn tất cả lại, tổng chi phí dành cho ăn uống và giải trí hàng tháng của bạn đã tăng vọt từ ba triệu lên tới hơn bảy triệu rưỡi.')
add_s('Bóc thực trạng', 'GFX', 'Dòng chữ cảnh báo tài chính: Rò rỉ vi mô là con dao sắc nhọn cắt đứt dòng tiền tích lũy', 8, 'Những khoản chi tiêu nhỏ lẻ này không bao giờ ập đến như một cú sốc lớn, mà ngấm ngầm bào mòn dòng tiền của bạn từng ngày.')

# --- Khoản 3: Phương tiện & Di chuyển (Scenes 025 - 032) ---
add_s('Bóc thực trạng', 'IMG', 'Chiếc xe máy số giản dị dựng trước sảnh văn phòng của những ngày đầu đi làm', 8, 'Hạng mục nâng cấp thứ ba thường xuất hiện khi thu nhập gia tăng chính là phương tiện đi lại và cách thức bạn di chuyển mỗi ngày.')
add_s('Bóc thực trạng', 'IMG', 'Chiếc xe tay ga cao cấp mới toanh bóng loáng với biển số mới trong bãi đỗ xe', 8, 'Bạn bắt đầu có cảm giác chiếc xe máy số cũ kỹ thời sinh viên không còn xứng tầm với mức lương hai mươi triệu và vị trí hiện tại.')
add_s('Bóc thực trạng', 'GFX', 'Hợp đồng mua xe trả góp: Trả trước một phần, mỗi tháng trả góp ngân hàng hai triệu rưỡi trong hai năm', 8, 'Bạn quyết định tậu ngay một chiếc xe tay ga cao cấp theo hình thức trả góp hai triệu rưỡi mỗi tháng vì đinh ninh mình thừa sức chi trả.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật ngồi trong xe taxi công nghệ nhìn mưa rơi ngoài cửa kính trên đường đi làm', 8, 'Vào những hôm thời tiết mưa gió hay nắng gắt, thay vì mặc áo mưa tự lái xe, bạn bắt đầu hình thành phản xạ mở điện thoại đặt taxi công nghệ.')
add_s('Bóc thực trạng', 'GFX', 'Lịch sử chuyến đi đặt xe: Mỗi tuần bốn cuốc xe ô tô, một tháng tiêu tốn thêm một triệu hai trăm nghìn', 8, 'Bạn tự nhủ rằng sức khỏe và sự tiện nghi là quan trọng, nhưng thực tế mỗi tháng bạn đã tốn thêm một triệu hai trăm nghìn cho các chuyến xe ô tô.')
add_s('Bóc thực trạng', 'GFX', 'Bảng tính chi phí xe cộ: Xăng, bảo dưỡng định kỳ, phí gửi xe chung cư và trả góp tổng cộng bốn triệu mỗi tháng', 8, 'Chi phí vận hành phương tiện tăng vọt từ năm trăm nghìn đồng trước kia lên mức bốn triệu đồng mỗi tháng, gấp tám lần mức chi tiêu ban đầu.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật đứng nhìn bảng giá gửi xe và tiền bảo hiểm xe máy tại bàn tiếp tân với vẻ mặt đăm chiêu', 8, 'Bất kỳ món đồ đắt tiền nào bạn sở hữu cũng đều kéo theo một hệ sinh thái các chi phí phụ trợ đắt đỏ đi cùng để duy trì nó.')
add_s('Bóc thực trạng', 'GFX', 'Sơ đồ bẫy chi phí bảo trì: Mua tài sản giá cao luôn đi kèm chi phí vận hành giá cao', 8, 'Khi bạn nâng cấp chiếc xe, bạn không đơn thuần chỉ chi tiền mua xe, mà bạn đã tự ký cam kết gánh thêm một chuỗi chi phí định kỳ dài hạn.')

# --- Khoản 4: Mua sắm cá nhân & Đồ công nghệ (Scenes 033 - 040) ---
add_s('Bóc thực trạng', 'IMG', 'Hộp đựng chiếc điện thoại thông minh cao cấp đời mới nhất vừa được mở hộp trên bàn làm việc', 8, 'Hạng mục thứ tư là mua sắm cá nhân và đồ công nghệ, nơi chiếc bẫy tâm lý mang tên mình xứng đáng được kích hoạt mạnh mẽ nhất.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật đeo chiếc đồng hồ thông minh và tai nghe không dây đời mới, cảm thấy tự tin trước gương', 8, 'Bạn nâng cấp lên chiếc điện thoại thông minh đời mới nhất ba mươi triệu đồng, sắm thêm đồng hồ thông minh và tai nghe không dây cho đủ bộ.')
add_s('Bóc thực trạng', 'GFX', 'Hóa đơn mua sắm trả góp thẻ tín dụng: Ba mươi lăm triệu chia đều cho mười hai tháng, mỗi tháng ba triệu', 8, 'Bạn chia nhỏ số tiền lớn đó thành các đợt trả góp lãi suất không phần trăm qua thẻ tín dụng, tự nhủ mỗi tháng chỉ tốn có vài triệu đồng.')
add_s('Bóc thực trạng', 'IMG', 'Tủ quần áo đầy ắp những bộ trang phục công sở đắt tiền có thương hiệu nổi tiếng', 8, 'Trong tủ đồ của bạn bắt đầu xuất hiện những chiếc áo sơ mi, đôi giày da hàng hiệu có mức giá đắt gấp ba lần những món đồ ngày trước.')
add_s('Bóc thực trạng', 'IMG', 'Thẻ hội viên phòng tập thể hình cao cấp nằm trong ví, nhưng bên cạnh là lịch sử chỉ mới tập được ba buổi', 8, 'Bạn mạnh tay mua thẻ tập gym cao cấp mười hai triệu đồng một năm, nhưng chỉ sau một tháng đầu tiên bạn hầu như không còn lui tới tập luyện.')
add_s('Bóc thực trạng', 'GFX', 'Biểu đồ chi tiêu ngẫu hứng: Các khoản mua sắm và đồ công nghệ tiêu tốn trung bình ba triệu rưỡi mỗi tháng', 8, 'Tính trung bình, các khoản chi tiêu mua sắm ngẫu hứng này đã âm thầm cắn vào ngân sách của bạn thêm ba triệu rưỡi mỗi tháng một cách đều đặn.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật cầm điện thoại lướt các sàn thương mại điện tử vào đêm khuya, bấm đặt hàng liên tục', 8, 'Thói quen lướt sàn thương mại điện tử ban đêm trở thành công cụ giải tỏa áp lực công việc, nhưng nó để lại những đơn hàng không thực sự cần thiết.')
add_s('Bóc thực trạng', 'GFX', 'Chỉ số hưng phấn ngắn hạn: Cảm giác thỏa mãn chỉ kéo dài vài ngày nhưng nợ thẻ kéo dài nhiều tháng', 8, 'Cảm giác hưng phấn khi đập hộp món đồ mới chỉ kéo dài vài ngày ngắn ngủi, nhưng nghĩa vụ trả nợ sẽ đeo bám bạn suốt sáu tháng đến một năm.')

# --- Khoản 5: Chi phí xã giao & Duy trì hình ảnh (Scenes 041 - 048) ---
add_s('Bóc thực trạng', 'IMG', 'Nhóm bạn trẻ cùng nhau trò chuyện vui vẻ tại quán cà phê tầng thượng sang trọng nhìn ra thành phố', 8, 'Khoản chi tiêu cuối cùng trong năm hạng mục nâng cấp vô thức chính là chi phí xã giao, ăn nhậu và duy trì hình ảnh bề ngoài của bản thân.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật rút ví đặt tờ tiền mệnh giá năm trăm nghìn lên bàn góp tiền tiệc cùng đồng nghiệp', 8, 'Khi đảm nhận vị trí công việc mới, bạn thấy rất khó để chối từ những buổi tiệc sau giờ làm việc hoặc các chuyến đi dã ngoại cuối tuần cùng nhóm.')
add_s('Bóc thực trạng', 'GFX', 'Hóa đơn tiệc tùng: Hai buổi gặp gỡ đối tác và đồng nghiệp cuối tuần tiêu tốn hai triệu đồng', 8, 'Mỗi lần tham gia ăn uống cùng nhóm đồng nghiệp hay đối tác, số tiền chia hóa đơn cho mỗi người chưa bao giờ dưới năm trăm nghìn đến một triệu đồng.')
add_s('Bóc thực trạng', 'IMG', 'Chiếc phong bì mừng cưới in hoa văn sang trọng kèm lời chúc mừng đồng nghiệp thân thiết', 8, 'Tiền mừng cưới hỏi, sinh nhật hay quà biếu đối tác cũng được bạn chủ động nâng mức tiền lên để tương xứng với mức thu nhập hai mươi triệu.')
add_s('Bóc thực trạng', 'GFX', 'Bảng thống kê chi phí xã giao: Tăng từ một triệu lên ba triệu rưỡi mỗi tháng để giữ gìn quan hệ', 8, 'Khoản ngân sách ngoại giao vô hình này đã tiêu tốn thêm khoảng hai triệu rưỡi mỗi tháng, vượt xa khả năng tích lũy thực tế của bạn.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật nhìn vào gương trong phòng vệ sinh nhà hàng, nụ cười gượng gạo che giấu sự lo lắng bên trong', 8, 'Bạn đang phải gồng mình chi trả những khoản tiền đắt đỏ chỉ để gìn giữ một vỏ bọc thành đạt trước ánh nhìn của những người xung quanh.')
add_s('Bóc thực trạng', 'GFX', 'Bảng cân đối thu chi tổng kết 5 hạng mục: Nhà ở tăng sáu triệu, Ăn uống tăng bốn triệu, Xe cộ tăng ba triệu rưỡi, Mua sắm tăng ba triệu rưỡi, Xã giao tăng hai triệu rưỡi', 10, 'Nhìn lại toàn bộ bức tranh: Toàn bộ mười triệu đồng tiền lương tăng thêm đã bị nuốt chửng hoàn toàn bởi năm hạng mục nâng cấp vô thức này.')
add_s('Bóc thực trạng', 'GFX', 'Dòng số liệu đỏ rực: Thu nhập hai mươi triệu, Tổng chi tiêu hai mươi triệu, Số dư cuối tháng bằng không', 8, 'Đó chính là câu trả lời vì sao dù lương của bạn có tăng gấp đôi, nhưng ví tiền của bạn vẫn hoàn toàn rỗng không vào mỗi cuối tháng.')

# =========================================================================
# BEAT 3: SỐ LIỆU & GIẢI PHẪU 3 BẪY TÂM LÝ (Scenes 049 - 096, 48 scenes)
# =========================================================================
# --- Bẫy 1: Cỗ máy thích nghi khoái lạc (Scenes 049 - 062) ---
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật chạy trên chiếc máy chạy bộ trong phòng tập, mồ hôi rơi nhưng vẫn đứng yên một chỗ', 8, 'Vì sao một người có học vấn, thông minh và có thu nhập rất tốt lại dễ dàng rơi vào cái bẫy chi tiêu luẩn quẩn này?')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Tiêu đề đồ họa nổi bật: Bẫy tâm lý số 1 - Cỗ máy thích nghi khoái lạc', 8, 'Nguyên nhân nằm ở một hiện tượng tâm lý học hành vi vô cùng nổi tiếng mang tên cỗ máy thích nghi khoái lạc của con người.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Biểu đồ sóng cảm xúc: Cột mốc hạnh phúc tăng vọt khi mua nhà mới rồi tụt dốc trở về mức cân bằng ban đầu sau 30 ngày', 8, 'Bộ não con người có xu hướng thích nghi cực kỳ nhanh chóng trước bất kỳ sự tiện nghi hay điều kiện sung túc vật chất mới nào.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật thức dậy trong căn hộ chung cư mới, nhìn quanh căn phòng với vẻ mặt bình thường, không còn hào hứng', 8, 'Khi bạn chuyển từ phòng trọ sang căn hộ chung cư sáu triệu đồng, trong tuần đầu tiên bạn cảm thấy tràn ngập sự hứng khởi và mãn nguyện.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật ngồi tại ban công chung cư lướt điện thoại, cảm thấy căn hộ bắt đầu có những điểm chật chội và bất tiện', 8, 'Nhưng chỉ sau đúng ba mươi ngày sinh sống, căn hộ sang trọng ấy nhanh chóng trở thành tiêu chuẩn hiển nhiên và bình thường mới trong mắt bạn.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Mô hình bậc thang thích nghi: Tiêu chuẩn sống tăng lên vĩnh viễn, nhưng cảm giác thỏa mãn lập tức biến mất', 8, 'Bạn không còn cảm thấy hạnh phúc hơn trước, nhưng bạn lại tuyệt đối không bao giờ chấp nhận quay về sống ở căn phòng trọ nhỏ ngày xưa.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật nhìn sang tòa nhà chung cư cao cấp bên cạnh với ánh mắt ao ước một căn hộ rộng hơn', 8, 'Và thế là, bạn lại bắt đầu khao khát một căn hộ cao cấp hơn nữa với giá mười triệu đồng để tìm lại cảm giác hưng phấn ban đầu.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Biểu đồ vòng lặp luẩn quẩn: Kiếm nhiều tiền hơn -> Tiêu nhiều hơn -> Cần kiếm nhiều hơn để duy trì', 8, 'Hiện tượng này giống như việc chạy trên máy tập: Đôi chân bạn guồng càng nhanh, nhưng vị trí thực tế của bạn thì vẫn dậm chân tại chỗ.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật mệt mỏi tựa lưng vào ghế văn phòng sau giờ làm, cảm thấy bị mắc kẹt trong guồng quay công việc', 8, 'Bạn buộc phải làm việc nhiều giờ hơn, gánh vác nhiều căng thẳng hơn chỉ để duy trì mức sống xa hoa mà chính mình đã tự tạo ra.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Đồ thị phân tích: Chi phí nâng cấp thì vĩnh viễn, nhưng niềm vui nâng cấp chỉ là tạm thời', 8, 'Đây là chiếc bẫy nguy hiểm nhất: Chúng ta phải đánh đổi tiền bạc tích lũy thật để mua lấy những cảm xúc hưng phấn vô cùng ngắn ngủi.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật cầm cốc nước lọc ngồi suy ngẫm bên bàn làm việc tĩnh lặng', 8, 'Nếu không nhận thức rõ cơ chế này, thì dù lương bạn có chạm mốc năm mươi triệu đồng, bạn vẫn sẽ tiêu sạch năm mươi triệu mỗi tháng.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Quy luật thích nghi của não bộ: Mức sống tăng lên như van một chiều, rất dễ mở ra nhưng cực kỳ khó đóng lại', 8, 'Kinh tế học gọi đây là tính bất đối xứng trong tiêu dùng: Nâng mức sống lên chỉ mất một ngày, nhưng hạ xuống thì mất cả năm trời đau đớn.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật thở dài nhìn danh sách các khoản thanh toán cố định tự động trừ tiền trong ứng dụng ngân hàng', 8, 'Những khoản chi tiêu xa xỉ khi đã trở thành thói quen sẽ bị tâm trí đánh tráo thành những nhu cầu sinh hoạt thiết yếu giả tạo.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Thông điệp khắc cốt ghi tâm: Làm chủ cỗ máy thích nghi là bước đầu tiên để giành lại tự do tài chính', 8, 'Hiểu rõ và làm chủ được cỗ máy thích nghi này chính là chiếc chìa khóa sống còn giúp bạn chặn đứng đà phá sản thầm lặng của bản thân.')

# --- Bẫy 2: Hiệu ứng Đi-đơ-rô (Scenes 063 - 076) ---
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Bức chân dung triết gia Đi-đơ-rô thời kỳ Khai sáng thế kỷ mười tám trong phòng làm việc cổ kính', 8, 'Bẫy tâm lý số hai sẽ giải thích vì sao chỉ một món đồ mới mua lại có thể châm ngòi cho cả một chuỗi chi tiêu thảm họa.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Tiêu đề đồ họa: Bẫy tâm lý số 2 - Hiệu ứng Đi-đơ-rô và phản ứng dây chuyền mua sắm', 8, 'Chiếc bẫy này mang tên Hiệu ứng Đi-đơ-rô, bắt nguồn từ câu chuyện có thật của một triết gia người Pháp vĩ đại vào thế kỷ mười tám.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Hình minh họa chiếc áo choàng nhung đỏ rực rỡ tuyệt đẹp được tặng đặt giữa căn phòng làm việc cũ kỹ', 8, 'Ông sống cả đời thanh đạm và giản dị, cho đến khi bất ngờ được một người bạn quý tặng cho chiếc áo choàng nhung đỏ lộng lẫy.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Sơ đồ tương phản: Chiếc áo choàng nhung đỏ sang trọng làm nổi bật sự cũ kỹ của bàn ghế và đồ đạc xung quanh', 8, 'Khi khoác chiếc áo choàng lộng lẫy lên người, ông lập tức nhìn căn phòng cũ kỹ của mình với cảm giác kệch cỡm và không tương xứng.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Triết gia Đi-đơ-rô đứng thay thế chiếc bàn làm việc cũ bằng chiếc bàn gỗ quý đắt tiền', 8, 'Để xứng với chiếc áo nhung đỏ, ông quyết định thay chiếc bàn làm việc bằng một chiếc bàn gỗ quý chạm khắc đắt đỏ hơn.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Phản ứng dây chuyền mua sắm: Áo choàng đỏ kéo theo Bàn mới, Thảm dệt mới, Tranh treo tường mới và Ghế bọc da mới', 8, 'Có bàn mới, ông lại thấy tấm thảm cũ không hợp, liền mua thêm thảm dệt, tranh treo tường và toàn bộ ghế bọc da sang trọng.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Triết gia Đi-đơ-rô ngồi gục đầu giữa căn phòng nguy nga lộng lẫy nhưng ngập trong đống nợ nần', 8, 'Kết quả cuối cùng là vị triết gia thông thái đã khánh kiệt toàn bộ tiền bạc chỉ vì muốn hoàn thiện sự đồng bộ cho chiếc áo choàng.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Ví dụ thực tế thời hiện đại: Mua điện thoại thông minh 30 triệu kéo theo Ốp lưng xịn, Củ sạc nhanh, Đồng hồ thông minh và Tai nghe cao cấp', 8, 'Trong đời sống hiện đại, khi bạn mua một chiếc điện thoại ba mươi triệu, bạn lập tức mua thêm củ sạc nhanh, ốp lưng và tai nghe đắt tiền.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật đứng ngắm chiếc xe tay ga mới và chuẩn bị mua thêm mũ bảo hiểm nhập khẩu cùng áo khoác đắt tiền', 8, 'Mua xe tay ga mới thì phải sắm mũ bảo hiểm nhập khẩu và áo khoác hàng hiệu; thuê căn hộ mới thì phải mua thêm máy lọc không khí và robot hút bụi.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Đồ thị phân tích chi phí phái sinh: Món đồ ban đầu chỉ chiếm 40% chi phí, 60% chi phí còn lại đến từ chuỗi mua sắm phái sinh', 8, 'Mỗi lần mua sắm một món đồ vượt chuẩn, bạn vô tình khởi động một phản ứng dây chuyền chi tiêu phái sinh kéo theo sau đó.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Quy luật mắt xích tiêu dùng: Một tài sản nâng cấp luôn đòi hỏi toàn bộ tài sản xung quanh phải nâng cấp đồng bộ', 8, 'Tâm lý muốn mọi thứ xung quanh phải đồng bộ về đẳng cấp chính là thủ phạm khiến tiền bạc của bạn bay màu với tốc độ chóng mặt.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật quyết đoán đặt chiếc điện thoại xuống bàn, từ chối bấm mua món đồ phụ kiện không cần thiết', 8, 'Để thoát khỏi hiệu ứng này, bạn phải học cách chặt đứt phản ứng dây chuyền ngay từ mắt xích mua sắm đầu tiên.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Nguyên tắc vàng chống bẫy Đi-đơ-rô: Chấp nhận sự không hoàn hảo và kiên quyết nói không với việc nâng cấp đồng bộ', 8, 'Đừng bao giờ mua thêm đồ đạc chỉ để làm cho nó tương xứng với một món đồ xa xỉ khác mà bạn vừa mới sở hữu.')

# --- Bẫy 3: Định luật Pắc-kin-xơn (Scenes 077 - 096) ---
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Chân dung nhà sử học và kinh tế học Cyril Parkinson tại bàn làm việc với tập tài liệu dày cộp', 8, 'Bẫy tâm lý số ba là một định luật kinh tế học vô cùng tàn nhẫn được đặt theo tên của học giả Cyril Parkinson.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Tiêu đề đồ họa: Bẫy tâm lý số 3 - Định luật Pắc-kin-xơn về sự phình to của chi tiêu', 8, 'Định luật Pắc-kin-xơn phát biểu một chân lý đơn giản: Chi tiêu luôn tự động phình to ra để lấp đầy toàn bộ mức thu nhập sẵn có.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Minh họa bình nước và chất lỏng: Nước luôn giãn nở để chiếm trọn thể tích của bình chứa bất kể bình lớn hay nhỏ', 8, 'Giống như chất khí hay chất lỏng, tiền bạc trong tài khoản sẽ luôn tìm mọi lý do để tiêu tan hết bất kể bạn kiếm được bao nhiêu.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật nhớ lại thời sinh viên chỉ có năm triệu đồng mỗi tháng nhưng vẫn sống đủ và không hề nợ nần', 8, 'Khi bạn chỉ có thu nhập năm triệu đồng mỗi tháng thời sinh viên, bạn vẫn có cách để sinh tồn và xoay xở qua ngày.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật ngồi nhìn bảng sao kê thu nhập hai mươi triệu đồng nhưng vẫn tiêu sạch không còn một đồng', 8, 'Nhưng khi thu nhập tăng lên hai mươi triệu, não bộ của bạn sẽ tự động nghĩ ra hàng tá nhu cầu cấp bách mới để tiêu sạch số tiền đó.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'So sánh hai người A và B: Người A lương 15 triệu tiết kiệm 3 triệu vs Người B lương 40 triệu tiết kiệm 0 đồng', 8, 'Đây là lý do một người kiếm mười lăm triệu có thể tiết kiệm ba triệu, trong khi người kiếm bốn mươi triệu lại không tích lũy được đồng nào.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Người A ăn mặc giản dị ung dung đọc sách, Người B lái xe sang nhưng mặt mày căng thẳng vì nợ nần', 8, 'Sự giàu có thực chất không được đo đếm bằng số tiền bạn kiếm được mỗi tháng, mà được quyết định bởi số tiền bạn giữ lại được.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Biểu đồ tích lũy tài sản thực tế: Số tiền giữ lại mới tạo nên giá trị tài sản ròng, không phải tổng doanh thu hay chức danh', 8, 'Thu nhập chỉ là dòng nước chảy qua sông, còn tài sản tích lũy được mới là hồ chứa giúp bảo vệ bạn trước những biến cố cuộc đời.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật mở ví thấy còn nhiều tiền liền hào phóng chi trả cho những món đồ ngẫu hứng ngoài kế hoạch', 8, 'Khi nhìn thấy tài khoản còn nhiều tiền, bạn sẽ hình thành tâm lý chủ quan và hạ thấp tiêu chuẩn kiểm soát chi tiêu của mình xuống.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Quy luật co giãn của ví tiền: Tiền còn trong tài khoản thanh toán là tiền sắp sửa bị tiêu đi', 8, 'Quy luật này chứng minh: Nếu bạn để tiền nhàn rỗi nằm chung trong tài khoản chi tiêu hàng ngày, chắc chắn số tiền đó sẽ bốc hơi.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật ngồi phân tích bảng sao kê ngân hàng ba tháng gần nhất, nhận ra vô số khoản chi vô bổ', 8, 'Những khoản chi không tên cứ thế xuất hiện liên tục chỉ vì bạn nghĩ đơn giản rằng: Mình đang có sẵn tiền trong ví.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Công thức tài chính sai lầm: Thu nhập trừ Chi tiêu bằng Tiết kiệm -> Tiết kiệm luôn bằng 0', 8, 'Nếu bạn áp dụng công thức: Lấy thu nhập trừ đi chi tiêu rồi mới tiết kiệm phần còn lại, thì kết quả tiết kiệm sẽ mãi mãi bằng không.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật cầm bút ghi nhớ công thức tài chính đảo ngược: Thu nhập trừ Tiết kiệm bằng Chi tiêu', 8, 'Để bẻ gãy định luật Pắc-kin-xơn, bạn bắt buộc phải đảo ngược công thức: Trích tiền tiết kiệm trước, chỉ được phép tiêu phần còn lại.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Bảng minh họa công thức mới: Lương 20 triệu -> Tự động chuyển 6 triệu vào tích lũy -> Chỉ tiêu trong 14 triệu', 8, 'Khi bạn chủ động khóa bớt số tiền có sẵn, chi tiêu của bạn sẽ buộc phải tự co lại trong giới hạn cho phép một cách tự nhiên.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật mỉm cười nhẹ nhõm khi thấy tài khoản tiết kiệm tăng đều đặn mỗi tháng mà cuộc sống vẫn đủ đầy', 8, 'Bạn sẽ vô cùng ngạc nhiên khi thấy rằng dù tiêu ít tiền hơn, chất lượng cuộc sống thực tế của bạn vẫn không hề suy giảm.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Thông điệp tổng kết Beat 3: Ba chiếc bẫy tâm lý đã lộ diện - Thích nghi khoái lạc, Hiệu ứng Đi-đơ-rô và Định luật Pắc-kin-xơn', 8, 'Nhận diện đầy đủ ba chiếc bẫy tâm lý này là tiền đề then chốt để chúng ta cùng nhau bước vào bài toán tính toán chi phí cơ hội.')

# =========================================================================
# BEAT 4: PHÂN TÍCH CHI PHÍ CƠ HỘI THỰC CHIẾN (Scenes 097 - 116, 20 scenes)
# =========================================================================
add_s('Chi phí cơ hội', 'IMG', 'Hai ngã rẽ cuộc đời: Một bên dẫn đến tài sản vững chắc, một bên dẫn đến vòng xoáy tiêu dùng kiệt quệ', 8, 'Bây giờ, chúng ta sẽ cùng nhau thực hiện bài toán tài chính quan trọng nhất: Đo lường chi phí cơ hội của mười triệu đồng tăng thêm.')
add_s('Chi phí cơ hội', 'GFX', 'Định nghĩa chi phí cơ hội: Giá trị của sự lựa chọn tốt nhất bị bỏ qua khi bạn quyết định tiêu tiền vào việc khác', 8, 'Chi phí cơ hội là cái giá vô hình đắt đỏ nhất: Khi bạn chọn tiêu mười triệu cho mức sống xa hoa, bạn đã vĩnh viễn đánh mất những gì?')
add_s('Chi phí cơ hội', 'IMG', 'Nhân vật tính nhẩm: Mười triệu đồng mỗi tháng tương đương một trăm hai mươi triệu đồng mỗi năm', 8, 'Mười triệu đồng tiền lương tăng thêm mỗi tháng tương đương với một trăm hai mươi triệu đồng tiền mặt nhàn rỗi trong một năm trời.')
add_s('Chi phí cơ hội', 'GFX', 'So sánh trực quan: Một trăm hai mươi triệu đồng tiêu dùng vs Một trăm hai mươi triệu đồng đem đi đầu tư tích sản', 8, 'Nếu đem số tiền đó đi tiêu dùng, bạn có mức sống sang chảnh; nhưng nếu đem đi đầu tư kỷ luật, kết quả sẽ hoàn toàn khác biệt.')
add_s('Chi phí cơ hội', 'GFX', 'Bảng tính lãi kép 5 năm: Tích lũy 10 triệu/tháng với lãi suất 10%/năm -> Sau 5 năm có 774 triệu đồng', 8, 'Với mức lợi nhuận mười phần trăm một năm, sau năm năm kiên trì tích lũy mười triệu mỗi tháng, bạn sẽ sở hữu hơn bảy trăm bảy mươi triệu đồng.')
add_s('Chi phí cơ hội', 'IMG', 'Người A 32 tuổi sở hữu sổ tiết kiệm và danh mục đầu tư gần 800 triệu đồng, tâm thế tự tin và an tâm', 8, 'Ở tuổi ba mươi hai, bảy trăm bảy mươi triệu đồng là một bệ đỡ tài chính vững chắc, giúp bạn hoàn toàn làm chủ tương lai của mình.')
add_s('Chi phí cơ hội', 'GFX', 'Bảng tính lãi kép 10 năm: Tích lũy 10 triệu/tháng sau 10 năm cán mốc 2.05 tỷ đồng tài sản thực tế', 8, 'Nếu tiếp tục duy trì kỷ luật đó trong mười năm, sức mạnh của lãi kép sẽ nhân số tiền tích lũy của bạn lên hơn hai tỷ đồng.')
add_s('Chi phí cơ hội', 'IMG', 'Người B 32 tuổi vẫn nợ thẻ tín dụng, lương tăng lên nhưng ví tiền rỗng không, lo sợ mất việc mỗi ngày', 8, 'Ngược lại, nếu thả nổi chi tiêu cho lạm phát lối sống, sau mười năm bạn sẽ vẫn trắng tay và nơm nớp lo sợ mỗi khi nghĩ đến thất nghiệp.')
add_s('Chi phí cơ hội', 'GFX', 'Biểu đồ cán cân tương lai: Hai tỷ đồng tài sản tự do tài chính vs Đống hóa đơn và đồ đạc mất giá theo thời gian', 8, 'Chi phí cơ hội thực sự của cốc cà phê sáu mươi lăm nghìn hay căn hộ sang trọng không phải là số tiền bạn bỏ ra hôm nay.')
add_s('Chi phí cơ hội', 'GFX', 'Công thức quy đổi thời gian: Một chiếc điện thoại 30 triệu tương đương 150 giờ lao động vất vả của bạn', 8, 'Nó chính là sự tự do, sự an tâm và những năm tháng nghỉ hưu sớm mà bạn đã vô tình ném qua cửa sổ một cách lãng phí.')
add_s('Chi phí cơ hội', 'IMG', 'Nhân vật đứng trước ngã tư thành phố lúc hoàng hôn, ngẫm nghĩ về những năm tháng tuổi trẻ đã qua', 8, 'Mỗi đồng tiền bạn chi tiêu vô tội vạ hôm nay chính là một phần tự do tương lai của bạn đang bị đem ra bán rẻ.')
add_s('Chi phí cơ hội', 'GFX', 'Khái niệm Lương theo giờ thực tế: Lương 20 triệu chia cho 200 giờ làm việc thực tế = 100 nghìn đồng/giờ', 8, 'Hãy quy đổi mọi món đồ bạn muốn mua ra số giờ làm việc: Với mức lương một trăm nghìn một giờ, chiếc điện thoại ba mươi triệu là ba trăm giờ làm việc.')
add_s('Chi phí cơ hội', 'IMG', 'Nhân vật nhìn chiếc áo hàng hiệu giá hai triệu đồng và tự hỏi: Liệu món đồ này có đáng giá 20 giờ làm việc?', 8, 'Tự hỏi bản thân: Bạn có sẵn sàng nai lưng làm việc cật lực hai mươi giờ liên tục chỉ để đổi lấy chiếc áo mặc vài lần rồi chán?')
add_s('Chi phí cơ hội', 'GFX', 'Thang đo giá trị: Đổi thời gian sống lấy đồ tiêu sản là giao dịch bất lợi nhất của đời người', 8, 'Tư duy quy đổi chi tiêu ra thời gian lao động sẽ là chiếc phanh hãm hữu hiệu nhất giúp bạn dừng ngay những quyết định bốc đồng.')
add_s('Chi phí cơ hội', 'IMG', 'Nhân vật mỉm cười nhẹ nhõm, từ chối lời mời tham gia buổi mua sắm xa xỉ không cần thiết', 8, 'Bạn sẽ bắt đầu quý trọng từng đồng tiền mình làm ra hơn, vì đằng sau mỗi đồng tiền đó là mồ hôi và quỹ thời gian hữu hạn của cuộc đời.')
add_s('Chi phí cơ hội', 'GFX', 'Biểu đồ đối sánh tự do tài chính: Người giữ tiền mua được thời gian rảnh rỗi, người tiêu xài bị thời gian trói buộc', 8, 'Người tiêu tiền mua tiện nghi ngắn hạn, nhưng người tích lũy tiền bạc là người mua lại được chính sự tự do và thời gian sống của mình.')
add_s('Chi phí cơ hội', 'IMG', 'Nam MC đại diện kênh chỉ tay về phía trước, mở ra phần lộ trình hành động cụ thể từng bước', 8, 'Vậy làm thế nào để bẻ gãy chiếc bẫy lạm phát lối sống và giữ lại trọn vẹn số tiền lương tăng thêm? Đây là lộ trình ba bước dành cho bạn.')
add_s('Chi phí cơ hội', 'GFX', 'Tiêu đề đồ họa nổi bật: Lộ trình 3 tầng phòng thủ bảo vệ tài chính trước lạm phát lối sống', 8, 'Lộ trình ba tầng phòng thủ này được thiết kế để vận hành hoàn toàn tự động, không đòi hỏi bạn phải có ý chí thép hay hy sinh quá nhiều.')
add_s('Chi phí cơ hội', 'IMG', 'Nhân vật chuẩn bị sổ tay và bút, sẵn sàng áp dụng hệ thống quản lý tài chính mới vào thực tế', 8, 'Hãy chuẩn bị sẵn sàng ghi chép lại ba nguyên tắc hành động thực chiến này để áp dụng ngay vào kỳ nhận lương tiếp theo của bạn.')
add_s('Chi phí cơ hội', 'GFX', 'Tổng kết Beat 4: Từ bỏ chi tiêu vô thức để đổi lấy tài sản hai tỷ đồng và sự an tâm tuyệt đối', 8, 'Khi bạn đã thấu hiểu chi phí cơ hội, việc từ chối những cám dỗ nâng cấp lối sống sẽ trở nên nhẹ nhàng và tự nhiên hơn bao giờ hết.')

# =========================================================================
# BEAT 5: LỘ TRÌNH 3 TẦNG PHÒNG THỦ THỰC CHIẾN (Scenes 117 - 148, 32 scenes)
# =========================================================================
# --- Tầng 1: Quy tắc 48h & Giữ mức sống cũ thêm 6 tháng (Scenes 117 - 126) ---
add_s('Lộ trình hành động', 'GFX', 'Tiêu đề đồ họa: Tầng phòng thủ số 1 - Quy tắc đóng băng mức sống cũ trong sáu tháng đầu tiên', 8, 'Tầng phòng thủ đầu tiên mang tên: Đóng băng mức sống cũ trong ít nhất sáu tháng kể từ ngày bạn nhận quyết định tăng lương.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật nhận thông báo tăng lương nhưng vẫn tiếp tục ở căn phòng trọ cũ và đi chiếc xe máy quen thuộc', 8, 'Khi nhận quyết định tăng lương, hãy sống như thể mức lương mới vẫn chưa từng xuất hiện trong cuộc sống của bạn.')
add_s('Lộ trình hành động', 'GFX', 'Nguyên tắc vàng: Giữ nguyên chỗ ở, giữ nguyên phương tiện đi lại, giữ nguyên thói quen ăn uống trong 180 ngày', 8, 'Giữ nguyên tiền thuê nhà, giữ nguyên chiếc xe máy hiện tại và giữ nguyên thói quen ăn uống quen thuộc trong đúng một trăm tám mươi ngày.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật thở phào nhẹ nhõm vì không bị cuốn vào cơn lốc chuyển nhà hay mua xe trả góp vội vã', 8, 'Khoảng thời gian đóng băng sáu tháng này giúp bạn có đủ độ lùi tâm lý để bình tĩnh quan sát và xây dựng kế hoạch sử dụng tiền bạc.')
add_s('Lộ trình hành động', 'GFX', 'Đồ thị tích lũy ban đầu: Sau 6 tháng đóng băng, tài khoản tích lũy có ngay 60 triệu đồng làm quỹ đệm an toàn', 8, 'Chỉ sau sáu tháng đầu tiên, bạn đã có sẵn sáu mươi triệu đồng tiền mặt tích lũy trong tay để làm một tấm đệm tài chính dự phòng vững chắc.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật cầm điện thoại định bấm mua món đồ đắt tiền nhưng nhớ ra quy tắc liền dừng tay lại', 8, 'Song song với đó, hãy áp dụng triệt để quy tắc đóng băng bốn mươi tám giờ cho bất kỳ món đồ mua sắm cá nhân nào trên một triệu đồng.')
add_s('Lộ trình hành động', 'GFX', 'Quy tắc đóng băng 48 giờ: Trì hoãn mua sắm 48h để cảm xúc lắng xuống -> 80% ham muốn mua sắm sẽ tự biến mất', 8, 'Khi muốn mua một món đồ mới, hãy ép bản thân chờ đợi đủ bốn mươi tám giờ trước khi tiến hành thanh toán tiền.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật xóa món đồ khỏi giỏ hàng trực tuyến sau hai ngày suy nghĩ, cảm thấy nhẹ nhõm vì không tốn tiền', 8, 'Hơn tám mươi phần trăm những cơn bốc đồng mua sắm sẽ tự động nguội lạnh và biến mất sau hai ngày suy ngẫm tỉnh táo.')
add_s('Lộ trình hành động', 'GFX', 'Bộ lọc 3 câu hỏi trước khi chi tiền: Mình có thực sự cần nó? Mình sẽ dùng nó bao nhiêu lần? Có cách nào thay thế không?', 8, 'Trước khi rút ví, hãy tự vấn bản thân ba câu: Món này là nhu cầu hay sở thích? Mình sẽ dùng nó bao nhiêu lần một tuần?')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật mỉm cười tự tin, bước ra khỏi cửa hàng thời trang mà không mang theo bất kỳ túi đồ thừa thãi nào', 8, 'Nếu câu trả lời không thực sự thuyết phục, hãy dứt khoát quay lưng bước đi và giữ lại số tiền quý giá đó trong tài khoản của bạn.')

# --- Tầng 2: Hệ thống 3 tài khoản tự động & Trả cho mình trước (Scenes 127 - 136) ---
add_s('Lộ trình hành động', 'GFX', 'Tiêu đề đồ họa: Tầng phòng thủ số 2 - Thiết lập hệ thống 3 tài khoản số tự động phân bổ dòng tiền', 8, 'Tầng phòng thủ thứ hai là xây dựng hệ thống phân bổ dòng tiền tự động bằng cách chia thu nhập vào ba tài khoản ngân hàng riêng biệt.')
add_s('Lộ trình hành động', 'GFX', 'Sơ đồ luồng tiền: Lương 20 triệu đổ về ngày 05 hàng tháng -> Tự động chia nhánh vào 3 tài khoản riêng biệt', 8, 'Đừng bao giờ để toàn bộ tiền lương nằm chung trong một tài khoản thanh toán duy nhất gắn liền với ứng dụng điện thoại của bạn.')
add_s('Lộ trình hành động', 'GFX', 'Tài khoản số 1: Tài khoản Tích sản & Đầu tư (50% tiền lương tăng thêm = 5 triệu đồng/tháng)', 8, 'Tài khoản số một là Tài khoản Tích sản: Ngay ngày nhận lương, hệ thống tự động trích năm triệu đồng vào tài khoản này để mua tài sản.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật cài đặt lệnh chuyển tiền định kỳ tự động trên ứng dụng ngân hàng vào ngày nhận lương hàng tháng', 8, 'Đặt lệnh trích tiền tự động định kỳ vào đúng ngày mùng năm hàng tháng, tiền sẽ được chuyển đi trước khi bạn kịp nhìn thấy nó trong ví.')
add_s('Lộ trình hành động', 'GFX', 'Tài khoản số 2: Tài khoản Chi tiêu Cố định & Sinh hoạt (12 triệu đồng/tháng)', 8, 'Tài khoản số hai là Tài khoản Chi tiêu Cố định: Dành riêng mười hai triệu đồng để chi trả các khoản bắt buộc như tiền nhà, tiền ăn và hóa đơn sinh hoạt.')
add_s('Lộ trình hành động', 'GFX', 'Tài khoản số 3: Tài khoản Nâng cấp Đời sống có kiểm soát (3 triệu đồng/tháng)', 8, 'Tài khoản số ba là Tài khoản Thưởng Nâng cấp: Dành ba triệu đồng còn lại để bạn thoải mái nâng cấp đời sống mà không hề cảm thấy tội lỗi.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật vui vẻ đi ăn uống cùng bạn bè bằng số tiền trong tài khoản nâng cấp mà không lo thâm hụt tiền tiết kiệm', 8, 'Bạn vẫn được quyền tận hưởng thành quả lao động của mình, nhưng sự tận hưởng đó nằm trong một hạn mức được kiểm soát chặt chẽ.')
add_s('Lộ trình hành động', 'GFX', 'Nguyên tắc bất di bất dịch: Tiền ở tài khoản nào chỉ tiêu cho mục đích đó, tuyệt đối không chuyển chéo', 8, 'Nguyên tắc vàng: Khi tiền ở Tài khoản Thưởng hết sạch, bạn buộc phải dừng các hoạt động ăn chơi và chờ đến kỳ nhận lương tháng sau.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật bình thản từ chối buổi nhậu phát sinh ngoài kế hoạch vì tài khoản giải trí tháng này đã chạm đáy', 8, 'Việc phân tách ranh giới rõ ràng giữa các tài khoản sẽ loại bỏ hoàn toàn khả năng tiêu lẹm vào phần tiền tích lũy thiêng liêng của bạn.')
add_s('Lộ trình hành động', 'GFX', 'Hiệu quả của hệ thống tự động: Loại bỏ yếu tố cảm xúc và sự đấu tranh tâm lý ra khỏi việc giữ tiền', 8, 'Hệ thống tự động hóa này giúp bạn giữ tiền một cách nhẹ nhàng và kỷ luật mà không cần phải phụ thuộc vào ý chí chủ quan mỗi ngày.')

# --- Tầng 3: Biến thu nhập tăng thêm thành tài sản sinh lời (Scenes 137 - 148) ---
add_s('Lộ trình hành động', 'GFX', 'Tiêu đề đồ họa: Tầng phòng thủ số 3 - Chuyển hóa dòng tiền nhàn rỗi thành cỗ máy tài sản sinh lời', 8, 'Tầng phòng thủ thứ ba và cũng là tầng phòng thủ cao nhất: Biến số tiền bạn giữ lại được thành một cỗ máy sinh lời tự động.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật mở ứng dụng đầu tư chứng chỉ quỹ trên điện thoại, theo dõi danh mục tài sản đang sinh lời ổn định', 8, 'Thay vì để tiền nằm im chịu trượt giá lạm phát, hãy đưa tiền vào các kênh tích sản an toàn và bền vững theo thời gian.')
add_s('Lộ trình hành động', 'GFX', 'Ba kênh tích sản nền tảng: Quỹ khẩn cấp gửi ngân hàng, Chứng chỉ quỹ cổ phiếu cân bằng và Vàng tích lũy', 8, 'Xây dựng danh mục tích sản đơn giản gồm ba chân kiềng: Quỹ khẩn cấp gửi ngân hàng, chứng chỉ quỹ đầu tư định kỳ và vàng vật chất tích lũy.')
add_s('Lộ trình hành động', 'GFX', 'Mục tiêu số 1: Xây dựng Quỹ khẩn cấp từ 3 đến 6 tháng chi phí sinh hoạt (tương đương 40 đến 70 triệu đồng)', 8, 'Bước đầu tiên là hoàn thành Quỹ khẩn cấp từ ba đến sáu tháng chi phí sinh hoạt để tạo lá chắn tâm lý an toàn tuyệt đối.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật ngủ ngon giấc ban đêm, không còn nỗi lo âu thường trực về tiền bạc hay nguy cơ rủi ro bất ngờ', 8, 'Khi đã có một tấm lá chắn tài chính vững chãi trong tay, bạn sẽ ngủ ngon giấc hơn và tâm thế làm việc cũng trở nên nhẹ nhõm hơn rất nhiều.')
add_s('Lộ trình hành động', 'GFX', 'Mục tiêu số 2: Mua tích sản chứng chỉ quỹ định kỳ hàng tháng theo phương pháp bình quân giá vốn', 8, 'Bước tiếp theo là trích tiền mua chứng chỉ quỹ đều đặn vào một ngày cố định trong tháng theo chiến lược bình quân giá vốn dài hạn.')
add_s('Lộ trình hành động', 'GFX', 'Cơ chế tích lũy tài sản: Tiền làm việc thay bạn ngày đêm, tạo ra nguồn thu nhập thụ động bền vững trong tương lai', 8, 'Những đồng tiền tích lũy được sẽ trở thành những người lính thầm lặng làm việc chăm chỉ ngày đêm để tạo ra dòng thu nhập mới cho bạn.')
add_s('Lộ trình hành động', 'IMG', 'Cây tài chính lớn dần từ mầm non thành cây cổ thụ vững chắc che chở cho gia đình và tương lai', 8, 'Cây tài chính của bạn sẽ lớn dần theo năm tháng, từ một mầm non nhỏ bé tích lũy ban đầu trở thành một cây cổ thụ che chở cho bạn.')
add_s('Lộ trình hành động', 'GFX', 'Biểu đồ chuyển đổi vị thế: Từ người làm việc kiếm tiền sang người có tiền bạc làm việc cho mình', 8, 'Bạn sẽ dần dần chuyển đổi vị thế thành công: Từ một người làm công ăn lương sang một người làm chủ có tài sản sinh sôi nảy nở.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật bước đi tự tin trên đường phố rực rỡ ánh bình minh, tâm thái ung dung và tự do tự tại', 8, 'Đó mới chính là đỉnh cao của việc tăng lương: Thu nhập gia tăng để phục vụ cho sự tự do đích thực của bạn, chứ không phải cho những món đồ xa xỉ.')
add_s('Lộ trình hành động', 'GFX', 'Bảng tóm tắt 3 tầng phòng thủ: 1. Đóng băng 6 tháng - 2. Tự động chia 3 tài khoản - 3. Tích sản sinh lời định kỳ', 8, 'Hãy ghi nhớ trọn vẹn ba tầng phòng thủ: Đóng băng lối sống cũ, tự động phân bổ ba tài khoản và kiên trì tích sản sinh lời đều đặn.')
add_s('Lộ trình hành động', 'IMG', 'Nhân vật ký cam kết tài chính cá nhân vào trang đầu cuốn sổ tay, quyết tâm thay đổi số phận tài chính', 8, 'Ngay hôm nay, hãy đặt bút cam kết với chính bản thân mình rằng bạn sẽ kiên quyết không để chiếc bẫy lạm phát lối sống dẫn dắt thêm một lần nào nữa.')

# =========================================================================
# BEAT 6: KẾT LUẬN & KÊU GỌI HÀNH ĐỘNG (Scenes 149 - 157, 9 scenes)
# =========================================================================
add_s('Kết luận & Kêu gọi hành động', 'IMG', 'Nam MC đại diện kênh ngồi đọc sách bên hiên nhà ngập tràn ánh nắng ấm áp, tâm thái an nhiên', 8, 'Tăng lương là một cơ hội tuyệt vời mà cuộc sống ban tặng cho những nỗ lực làm việc không ngừng nghỉ của bạn.')
add_s('Kết luận & Kêu gọi hành động', 'GFX', 'Thông điệp cốt lõi: Kiếm nhiều tiền là tài năng, nhưng giữ được tiền và nhân tiền mới là bản lĩnh thực chiến', 8, 'Tuy nhiên, kiếm được nhiều tiền mới chỉ là điều kiện cần; biết giữ tiền và bắt tiền phục vụ cho mình mới là bản lĩnh tài chính thực sự.')
add_s('Kết luận & Kêu gọi hành động', 'IMG', 'Hình ảnh chiếc ví da dày dặn chứa đựng sự tự do và an tâm, bên cạnh là cuốn sổ tay kế hoạch cuộc đời', 8, 'Đừng biến sự thăng tiến trong sự nghiệp thành một chiếc lồng son mạ vàng giam cầm tự do và thời gian sống quý giá của chính bạn.')
add_s('Kết luận & Kêu gọi hành động', 'AIV', 'Chàng trai văn phòng mỉm cười tự tin, bước ra khỏi văn phòng với phong thái tự do, ánh hoàng hôn chiếu rực rỡ', 6, 'Hãy để mỗi đồng lương tăng thêm trở thành từng viên gạch vững chắc xây dựng nên sự độc lập và tự do tài chính của bạn.')
add_s('Kết luận & Kêu gọi hành động', 'AIV', 'Chàng trai bắt tay người bạn đồng nghiệp, trao nhau ánh mắt khích lệ đầy năng lượng tích cực', 6, 'Bạn hoàn toàn có thể làm chủ tiền bạc, bắt đầu ngay từ những hành động nhỏ bé nhưng chuẩn xác trong hôm nay.')
add_s('Kết luận & Kêu gọi hành động', 'GFX', 'Checklist 3 hành động ngay hôm nay: 1. Tải app ngân hàng chia 3 tài khoản - 2. Đặt lệnh trích tự động 5 triệu - 3. Dừng nâng cấp xe và nhà', 8, 'Hãy tải ứng dụng ngân hàng, thiết lập lệnh trích tự động ngay trong chiều nay và kiên quyết nói không với mọi cám dỗ nâng cấp chỗ ở hay xe cộ.')
add_s('Kết luận & Kêu gọi hành động', 'IMG', 'Master Anchor mỉm cười ấm áp giơ tay chào tạm biệt khán giả trong khung hình tinh tế', 8, 'Nếu thấy video này hữu ích, hãy bấm đăng ký kênh Tiền Thực Chiến và chia sẻ video đến người bạn thân thiết nhất của bạn.')

print(f"Tổng số phân cảnh: {len(scenes)}")

# Ghi ra file script.md
lines = [
    "# Script — lam-phat-loi-song-luong-tang-tien-mat",
    "Kênh: Tiền Thực Chiến | Ngôn ngữ: vi | Mục tiêu: 20 phút | TTS: vieneu | Voice: Hải Đăng",
    ""
]

for s in scenes:
    lines.append(f"## Scene {s['num']:03d}")
    lines.append(f"- Beat: {s['beat']}")
    lines.append(f"- Loại dự kiến: {s['type']}")
    lines.append(f"- Visual concept: {s['concept']}")
    lines.append(f"- Duration ước tính: {s['dur']}s")
    lines.append(f"- Narration: \"{s['nar']}\"")
    lines.append("")

SCRIPT_PATH.write_text("\n".join(lines), encoding="utf-8")
print(f"✅ Đã ghi hoàn tất 157 scenes vào {SCRIPT_PATH}")
