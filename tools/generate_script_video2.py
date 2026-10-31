#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_script_video2.py — Generate complete 20-minute script for Video #2
Video: lam-phat-loi-song-luong-tang-tien-mat
Channel: tien-thuc-chien
Duration: 20 mins (~160 scenes)
Asset strategy: Ultra cost-saver (7 AIVs, 86 GFX, 67 IMG)
"""

import sys
from pathlib import Path

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
script_path = ROOT_DIR / "channels" / "tien-thuc-chien" / "videos" / "lam-phat-loi-song-luong-tang-tien-mat" / "script.md"

scenes = []

def add_s(beat, stype, concept, dur, nar):
    scenes.append({
        'num': len(scenes) + 1,
        'beat': beat,
        'type': stype,
        'concept': concept,
        'dur': dur,
        'nar': nar
    })

# ==================== BEAT 1: HOOK (Scenes 001 - 008, ~60s) ====================
add_s('Hook', 'AIV', 'Chàng trai văn phòng 27 tuổi mặc sơ mi trắng mỉm cười hạnh phúc khi nhận email thăng chức và tăng lương gấp đôi lên hai mươi triệu đồng', 6, 'Bạn vừa đạt cột mốc đáng nhớ: được tăng lương từ mười triệu lên hai mươi triệu.')
add_s('Hook', 'AIV', 'Chàng trai cùng nhóm bạn đồng nghiệp nâng ly cocktail ăn mừng tưng bừng tại quầy bar nhà hàng sang trọng giữa ánh đèn lung linh', 6, 'Bạn tự hào ăn mừng, cảm thấy những năm tháng cày cuốc cuối cùng đã được đền đáp.')
add_s('Hook', 'AIV', 'Chàng trai đứng giữa căn hộ chung cư mới thuê rộng rãi, ban công ngắm nhìn toàn cảnh thành phố lung linh về đêm', 6, 'Bạn chuyển sang căn hộ mới tiện nghi, tin rằng mức lương này sẽ giúp tích lũy lớn.')
add_s('Hook', 'AIV', 'Chàng trai thẫn thờ nhìn chằm chằm vào màn hình điện thoại vào ngày hai mươi tám cuối tháng, thông báo số dư tài khoản chỉ còn vài chục ngàn đồng', 6, 'Thế nhưng cuối tháng mở app, số dư tài khoản vẫn là con số không tròn trĩnh.')
add_s('Hook', 'AIV', 'Chàng trai ngồi một mình bên bàn làm việc ban đêm, xoa thái dương trĩu nặng âu lo, tự hỏi tiền của mình đã biến đi đâu', 6, 'Lương tăng gấp đôi, nhưng cảm giác hoang mang, bất an cuối tháng vẫn y nguyên như cũ.')
add_s('Hook', 'GFX', 'Đồ thị đường thẳng song song: Đường lương màu xanh tăng 100% chạy song song với đường chi tiêu màu đỏ tăng 100%', 8, 'Nghịch lý ở chỗ: Khi thu nhập của bạn tăng lên một bậc, thì mức sống và các khoản chi tiêu cũng lập tức tăng theo đúng một bậc tương ứng.')
add_s('Hook', 'GFX', 'Mô hình biểu tượng chiếc bẫy chuột bằng vàng phát sáng mang tên Lạm phát lối sống', 8, 'Trong tài chính cá nhân, đây được gọi là chiếc bẫy lạm phát lối sống, thứ âm thầm triệt tiêu mọi thành quả lao động của bạn.')
add_s('Hook', 'IMG', 'Nam MC đại diện kênh Tiền Thực Chiến mặc sơ mi trắng đeo thẻ bước vào khung hình với vẻ mặt kiên định, sẵn sàng phân tích', 8, 'Hôm nay, tôi sẽ cùng bạn bóc trần ba chiếc bẫy tâm lý vô hình này và xây dựng lộ trình ba tầng phòng thủ để giữ lại tiền.')

# ==================== BEAT 2: BÓC THỰC TRẠNG (Scenes 009 - 048, ~300s) ====================
# --- Khoản 1: Chỗ ở & Tiện ích cố định (Scenes 009 - 016) ---
add_s('Bóc thực trạng', 'IMG', 'Hình ảnh căn phòng trọ nhỏ đơn sơ nhưng ấm cúng của những ngày đầu mới đi làm', 7, 'Hãy nhìn lại thời điểm bạn vừa ra trường, đi làm với mức lương khởi điểm mười triệu đồng.')
add_s('Bóc thực trạng', 'GFX', 'Bảng kê chi tiêu cũ: Tiền thuê trọ hai triệu rưỡi, điện nước năm trăm ngàn, tổng cộng ba triệu mỗi tháng', 8, 'Khi đó, bạn thuê một căn phòng nhỏ hai triệu rưỡi mỗi tháng, chi tiêu chắt chiu và vẫn sống hoàn toàn ổn thỏa.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật đứng ngắm tòa nhà chung cư mini hiện đại có thang máy và bảo vệ túc trực', 8, 'Nhưng ngay khi nhận thông báo lương hai mươi triệu, ý nghĩ đầu tiên xuất hiện trong đầu bạn là: Mình phải chuyển chỗ ở.')
add_s('Bóc thực trạng', 'GFX', 'Hợp đồng thuê nhà mới: Tiền thuê sáu triệu, phí dịch vụ một triệu, điện nước giá thương mại, tổng chín triệu', 8, 'Bạn chuyển sang căn hộ dịch vụ sáu triệu đồng, cộng thêm tiền gửi xe và dịch vụ, mỗi tháng mất đứt chín triệu.')
add_s('Bóc thực trạng', 'GFX', 'Biểu đồ cán cân: Chi phí nhà ở tăng vọt gấp 3 lần từ 3 triệu lên 9 triệu đồng mỗi tháng', 8, 'Bạn tự biện minh rằng: Ở nơi đẹp hơn thì mới có tinh thần làm việc tốt hơn và xứng tầm với vị trí mới.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật ngồi trên chiếc ghế sofa mới đắt tiền trong căn hộ, xung quanh là hóa đơn tiền nhà và phí quản lý', 7, 'Nhưng bạn không nhận ra rằng: Nhà ở là một khoản chi phí cố định, một khi đã ký hợp đồng thì không thể hạ xuống được.')
add_s('Bóc thực trạng', 'GFX', 'Cột mốc thời gian: Mười tháng thuê nhà mới tiêu tốn chín mươi triệu đồng, tương đương gần một năm tiền lương cũ', 8, 'Chỉ riêng việc nâng cấp chỗ ở đã nuốt chửng sáu mươi triệu đồng tiền chênh lệch mỗi năm của bạn.')
add_s('Bóc thực trạng', 'GFX', 'Thước đo ngân sách: Tỷ trọng tiền thuê nhà chiếm tới 45% tổng thu nhập hàng tháng, mức báo động đỏ', 8, 'Nguyên tắc tài chính chuẩn chỉ cho phép tiền nhà chiếm tối đa ba mươi phần trăm thu nhập, nhưng bạn đã vượt ngưỡng an toàn.')

# --- Khoản 2: Ăn uống & Cà phê hàng ngày (Scenes 017 - 024) ---
add_s('Bóc thực trạng', 'IMG', 'Quán cà phê vỉa hè mộc mạc quen thuộc với cốc cà phê đen đá mười lăm ngàn đồng', 7, 'Hạng mục rò rỉ thứ hai, tinh vi hơn rất nhiều, chính là thói quen ăn uống và cà phê hàng ngày.')
add_s('Bóc thực trạng', 'IMG', 'Cốc cà phê thương hiệu cao cấp đặt trên bàn làm việc sang chảnh có giá sáu mươi lăm ngàn đồng', 7, 'Trước đây, bạn hài lòng với cốc cà phê vỉa hè mười lăm ngàn; nay bạn chuyển sang cà phê thương hiệu sáu mươi lăm ngàn mỗi sáng.')
add_s('Bóc thực trạng', 'GFX', 'Phép tính nhân: Chênh lệch năm mươi ngàn mỗi ngày, một tháng ba mươi ngày đốt thêm một triệu rưỡi tiền cà phê', 8, 'Mỗi ngày chênh lệch năm mươi ngàn đồng nghe có vẻ vô hại, nhưng một tháng nó ngốn của bạn thêm một triệu rưỡi.')
add_s('Bóc thực trạng', 'IMG', 'Bàn ăn trưa tại nhà hàng cùng đồng nghiệp trong văn phòng, hóa đơn thanh toán trên một trăm ngàn', 7, 'Bữa trưa công sở từ cơm bình dân ba mươi lăm ngàn được nâng cấp thành những bữa ăn nhà hàng cùng đồng nghiệp tám mươi đến một trăm ngàn.')
add_s('Bóc thực trạng', 'GFX', 'Biểu đồ so sánh chi phí ăn trưa: Cơm bình dân 900 ngàn mỗi tháng vs Nhà hàng 2.5 triệu mỗi tháng', 8, 'Chỉ riêng tiền ăn trưa, bạn đã chi thêm hơn một triệu sáu trăm ngàn đồng mỗi tháng mà hoàn toàn không để ý.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật quét mã QR thanh toán hóa đơn bữa tối thịnh soạn tại nhà hàng lẩu nướng cùng bạn bè', 8, 'Chưa kể những buổi liên hoan, ăn tối sang chảnh vào cuối tuần để tự thưởng sau những ngày làm việc áp lực.')
add_s('Bóc thực trạng', 'GFX', 'Biểu đồ rò rỉ dòng tiền: Tổng chi phí ăn uống giải trí tăng vọt từ 3 triệu lên 7.5 triệu đồng mỗi tháng', 8, 'Cộng tất cả lại, khoản tiền ăn uống và cà phê của bạn đã tăng thêm hơn bốn triệu đồng mỗi tháng.')
add_s('Bóc thực trạng', 'GFX', 'Dòng chữ cảnh báo tài chính: Rò rỉ vi mô là con dao sắc nhọn cắt đứt dòng tiền tích lũy', 7, 'Những khoản chi nhỏ nhặt này không bao giờ xuất hiện dưới dạng một cú sốc lớn, mà thấm dần như nước chảy qua kẽ tay.')

# --- Khoản 3: Phương tiện & Di chuyển (Scenes 025 - 032) ---
add_s('Bóc thực trạng', 'IMG', 'Chiếc xe máy số giản dị dựng trước sảnh văn phòng của những ngày đầu đi làm', 7, 'Khoản nâng cấp thứ ba thường xuất hiện khi lương tăng chính là phương tiện và cách bạn di chuyển.')
add_s('Bóc thực trạng', 'IMG', 'Chiếc xe tay ga cao cấp mới toanh bóng loáng với biển số mới trong bãi đỗ xe', 8, 'Bạn cảm thấy chiếc xe máy cũ không còn phù hợp với vị trí quản lý hoặc mức lương hai mươi triệu của mình nữa.')
add_s('Bóc thực trạng', 'GFX', 'Hợp đồng mua xe trả góp: Trả trước một phần, mỗi tháng trả góp ngân hàng hai triệu rưỡi trong hai năm', 8, 'Bạn quyết định đổi một chiếc xe tay ga đắt tiền, chọn hình thức trả góp hai triệu rưỡi mỗi tháng vì nghĩ mình thừa sức trả.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật ngồi trong xe taxi công nghệ nhìn mưa rơi ngoài cửa kính trên đường đi làm', 7, 'Những ngày trời mưa hoặc nắng gắt, thay vì mặc áo mưa tự lái xe, bạn bắt đầu hình thành thói quen đặt xe ô tô công nghệ.')
add_s('Bóc thực trạng', 'GFX', 'Lịch sử chuyến đi trên app: Mỗi tuần bốn cuốc xe ô tô, một tháng tiêu tốn thêm một triệu hai trăm ngàn', 8, 'Bạn tự nhủ thời gian và sức khỏe là vàng, nhưng một tháng bạn lại mất thêm một triệu hai cho việc đi lại bằng ô tô.')
add_s('Bóc thực trạng', 'GFX', 'Bảng tính chi phí xe cộ: Xăng, bảo dưỡng định kỳ, phí gửi xe chung cư và trả góp tổng cộng bốn triệu mỗi tháng', 8, 'Chi phí vận hành phương tiện tăng từ năm trăm ngàn lên bốn triệu đồng mỗi tháng, gấp tám lần so với trước đây.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật đứng nhìn bảng giá gửi xe và tiền bảo hiểm xe máy tại bàn tiếp tân với vẻ mặt đăm chiêu', 7, 'Mỗi đồ vật đắt tiền bạn sở hữu đều kéo theo một hệ sinh thái chi phí bảo trì và bảo dưỡng đắt tiền đi kèm.')
add_s('Bóc thực trạng', 'GFX', 'Sơ đồ bẫy chi phí bảo trì: Mua tài sản giá cao luôn đi kèm chi phí vận hành giá cao', 8, 'Khi bạn nâng cấp chiếc xe, bạn không chỉ trả tiền cho cái xe, mà bạn đang cam kết trả thêm một chuỗi chi phí dài hạn.')

# --- Khoản 4: Mua sắm cá nhân & Đồ công nghệ (Scenes 033 - 040) ---
add_s('Bóc thực trạng', 'IMG', 'Hộp đựng chiếc điện thoại thông minh cao cấp đời mới nhất vừa được bóc seal trên bàn làm việc', 8, 'Hạng mục thứ tư là mua sắm cá nhân và đồ công nghệ, nơi cái bẫy mình xứng đáng phát huy tác dụng mạnh nhất.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật đeo chiếc đồng hồ thông minh và tai nghe không dây đời mới, cảm thấy tự tin trước gương', 7, 'Bạn đổi chiếc điện thoại mới ba mươi triệu, mua thêm đồng hồ thông minh và tai nghe cao cấp để đồng bộ hệ sinh thái.')
add_s('Bóc thực trạng', 'GFX', 'Hóa đơn mua sắm trả góp thẻ tín dụng: Ba mươi lăm triệu chia đều cho mười hai tháng, mỗi tháng ba triệu', 8, 'Bạn chia nhỏ số tiền thành các khoản trả góp lãi suất không phần trăm qua thẻ tín dụng, tự nhủ mỗi tháng chỉ tốn vài triệu.')
add_s('Bóc thực trạng', 'IMG', 'Tủ quần áo đầy ắp những bộ trang phục công sở đắt tiền có thương hiệu nổi tiếng', 7, 'Tủ đồ của bạn bắt đầu xuất hiện những chiếc áo sơ mi, đôi giày da hàng hiệu có giá gấp hai đến ba lần đồ cũ.')
add_s('Bóc thực trạng', 'IMG', 'Thẻ hội viên phòng tập gym năm sao mạ vàng nằm trong ví, nhưng bên cạnh là lịch sử chỉ mới tập được ba buổi', 8, 'Bạn mua gói tập gym mười hai triệu một năm tại trung tâm thể thao cao cấp, nhưng sau tháng đầu tiên chỉ ghé qua đúng ba lần.')
add_s('Bóc thực trạng', 'GFX', 'Biểu đồ chi tiêu ngẫu hứng: Các khoản mua sắm và đồ công nghệ ngốn trung bình ba triệu rưỡi mỗi tháng', 8, 'Tổng cộng các khoản chi tiêu mua sắm cá nhân đã lấy đi của bạn thêm ba triệu rưỡi mỗi tháng một cách đều đặn.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật cầm điện thoại lướt các sàn thương mại điện tử vào đêm khuya, bấm đặt hàng liên tục', 7, 'Mua sắm trực tuyến trở thành một liều thuốc giảm căng thẳng sau những giờ làm việc mệt mỏi ở công ty.')
add_s('Bóc thực trạng', 'GFX', 'Chỉ số Dopamine ngắn hạn: Cảm giác thỏa mãn chỉ kéo dài vài ngày nhưng nợ thẻ kéo dài nhiều tháng', 8, 'Khoảnh khắc bóc hộp đồ mới mang lại niềm vui chớp nhoáng, nhưng nghĩa vụ thanh toán sẽ bám theo bạn suốt nửa năm trời.')

# --- Khoản 5: Chi phí xã giao & Duy trì hình ảnh (Scenes 041 - 048) ---
add_s('Bóc thực trạng', 'IMG', 'Nhóm bạn trẻ cùng nhau trò chuyện vui vẻ tại quán bar tầng thượng sang trọng nhìn ra thành phố', 8, 'Hạng mục cuối cùng trong năm khoản nâng cấp vô thức chính là chi phí xã giao và duy trì hình ảnh cá nhân.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật rút ví đặt tờ tiền mệnh giá năm trăm ngàn lên bàn góp tiền tiệc cùng đồng nghiệp', 7, 'Khi ở vị trí mới, bạn không thể từ chối những buổi tiệc sau giờ làm hoặc những chuyến dã ngoại cuối tuần cùng nhóm.')
add_s('Bóc thực trạng', 'GFX', 'Hóa đơn tiệc tùng: Hai buổi gặp gỡ đối tác và đồng nghiệp cuối tuần tiêu tốn hai triệu đồng', 8, 'Mỗi lần đi ăn uống cùng nhóm quản lý, tiền chia hóa đơn không bao giờ dưới năm trăm ngàn đến một triệu đồng.')
add_s('Bóc thực trạng', 'IMG', 'Chiếc phong bì mừng cưới in hoa văn sang trọng kèm lời chúc mừng đồng nghiệp thân thiết', 7, 'Tiền mừng cưới hỏi, sinh nhật của bạn bè và đồng nghiệp cũng được bạn nâng mức phong bì lên để không bị kém cạnh.')
add_s('Bóc thực trạng', 'GFX', 'Bảng thống kê chi phí xã giao: Tăng từ một triệu lên ba triệu rưỡi mỗi tháng để giữ gìn quan hệ', 8, 'Khoản chi phí ngoại giao vô hình này âm thầm ngốn thêm hai triệu rưỡi mỗi tháng từ thu nhập của bạn.')
add_s('Bóc thực trạng', 'IMG', 'Nhân vật nhìn vào gương trong phòng vệ sinh nhà hàng, nụ cười gượng gạo che giấu sự lo lắng bên trong', 8, 'Bạn đang phải gồng mình chi tiền để duy trì một vỏ bọc thành đạt trước mắt những người xung quanh.')
add_s('Bóc thực trạng', 'GFX', 'Bảng cân đối thu chi tổng kết 5 hạng mục: Nhà ở tăng sáu triệu, Ăn uống tăng bốn triệu, Xe cộ tăng ba triệu rưỡi, Mua sắm tăng ba triệu rưỡi, Xã giao tăng hai triệu rưỡi', 10, 'Hãy nhìn vào bức tranh tổng thể: Toàn bộ mười triệu tiền lương tăng thêm đã bị nuốt chửng hoàn toàn bởi năm hạng mục nâng cấp vô thức này.')
add_s('Bóc thực trạng', 'GFX', 'Dòng số liệu đỏ rực: Thu nhập hai mươi triệu, Tổng chi tiêu hai mươi triệu, Số dư cuối tháng bằng không', 8, 'Và đó chính là lý do vì sao lương bạn tăng gấp đôi, nhưng ví tiền của bạn vẫn rỗng không vào cuối tháng.')

# ==================== BEAT 3: SỐ LIỆU & GIẢI PHẪU 3 BẪY TÂM LÝ (Scenes 049 - 096, ~360s) ====================
# --- Bẫy tâm lý 1: Hedonic Treadmill (Scenes 049 - 062) ---
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật chạy trên chiếc máy chạy bộ trong phòng tập, mồ hôi rơi nhưng vẫn đứng yên một chỗ', 8, 'Tại sao một người thông minh, có học thức và có thu nhập tốt lại dễ dàng rơi vào cái bẫy này?')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Tiêu đề đồ họa nổi bật: Bẫy tâm lý số 1 - Cỗ máy chạy bộ khoái lạc Hedonic Treadmill', 8, 'Câu trả lời nằm ở hiện tượng tâm lý học kinh điển mang tên Hedonic Treadmill, hay cỗ máy chạy bộ khoái lạc.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Biểu đồ sóng cảm xúc: Cột mốc hạnh phúc tăng vọt khi mua nhà mới rồi tụt dốc trở về mức cân bằng ban đầu sau 30 ngày', 8, 'Bộ não con người có cơ chế thích nghi cực kỳ nhanh chóng với mọi sự tiện nghi và sung túc mới.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật thức dậy trong căn hộ chung cư mới, nhìn quanh căn phòng với vẻ mặt bình thường, không còn hào hứng', 7, 'Khi bạn chuyển từ phòng trọ sang chung cư sáu triệu, tuần đầu tiên bạn cảm thấy ngập tràn trong hạnh phúc.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật ngồi tại ban công chung cư lướt điện thoại, cảm thấy căn hộ bắt đầu có những điểm chật chội và bất tiện', 8, 'Nhưng chỉ sau ba mươi ngày, căn hộ đẹp đẽ này trở thành tiêu chuẩn bình thường mới trong mắt bạn.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Mô hình bậc thang thích nghi: Tiêu chuẩn sống tăng lên vĩnh viễn, nhưng cảm giác thỏa mãn lập tức biến mất', 8, 'Bạn không còn thấy hạnh phúc hơn trước, nhưng bạn lại không bao giờ có thể quay về sống ở căn phòng trọ cũ được nữa.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật nhìn sang tòa nhà chung cư cao cấp bên cạnh với ánh mắt ao ước một căn hộ rộng hơn', 8, 'Và thế là, bạn bắt đầu khao khát một căn hộ cao cấp hơn mười triệu để tìm lại cảm giác hưng phấn ban đầu.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Biểu đồ vòng lặp luẩn quẩn: Kiếm nhiều tiền hơn -> Tiêu nhiều hơn -> Cần kiếm nhiều hơn để duy trì', 8, 'Nó giống hệt như việc bạn chạy trên máy tập: Chân bạn guồng càng nhanh, nhưng vị trí của bạn thì vẫn dậm chân tại chỗ.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật mệt mỏi tựa lưng vào ghế văn phòng sau giờ làm, cảm thấy bị mắc kẹt trong guồng quay công việc', 7, 'Bạn phải làm việc nhiều giờ hơn, chịu nhiều áp lực hơn chỉ để nuôi sống mức sống mới mà mình đã lỡ tạo ra.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Đồ thị phân tích: Chi phí nâng cấp thì vĩnh viễn, nhưng niềm vui nâng cấp chỉ là tạm thời', 8, 'Đây chính là bẫy tâm lý nguy hiểm nhất: Chúng ta chi tiêu thật để mua những niềm vui ngắn hạn.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật cầm cốc nước lọc ngồi suy ngẫm bên bàn làm việc tĩnh lặng', 7, 'Nếu không nhận thức được cỗ máy này, dù lương bạn có lên năm mươi triệu, bạn vẫn sẽ tiêu sạch năm mươi triệu.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Quy luật thích nghi của não bộ: Mức sống tăng lên như van một chiều, rất dễ mở ra nhưng cực kỳ khó đóng lại', 8, 'Các nhà kinh tế học gọi đây là tính bất đối xứng của chi tiêu: Nâng lên thì mất một ngày, hạ xuống thì mất cả năm.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật thở dài nhìn danh sách các khoản thanh toán cố định tự động trừ tiền trong app ngân hàng', 7, 'Những khoản chi đã thành thói quen sẽ biến thành nhu cầu thiết yếu giả tạo trong tâm trí bạn.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Thông điệp khắc cốt ghi tâm: Làm chủ cỗ máy Hedonic Treadmill là bước đầu tiên để giành lại tự do tài chính', 8, 'Nhận ra được cỗ máy này đang vận hành chính là chìa khóa đầu tiên giúp bạn dừng lại trước khi quá muộn.')

# --- Bẫy tâm lý 2: Hiệu ứng Diderot (Scenes 063 - 076) ---
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Bức chân dung triết gia Denis Diderot thời kỳ Khai sáng thế kỷ mười tám trong phòng làm việc cổ kính', 8, 'Bẫy tâm lý số hai giải thích vì sao một món đồ nhỏ lại có thể kích hoạt cả một chuỗi chi tiêu thảm họa.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Tiêu đề đồ họa: Bẫy tâm lý số 2 - Hiệu ứng Diderot và phản ứng dây chuyền mua sắm', 8, 'Nó mang tên Hiệu ứng Diderot, bắt nguồn từ câu chuyện có thật của triết gia người Pháp Denis Diderot vào thế kỷ mười tám.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Hình minh họa chiếc áo choàng nhung đỏ rực rỡ tuyệt đẹp được tặng đặt giữa căn phòng làm việc cũ kỹ', 8, 'Diderot cả đời sống thanh bạch, cho đến một ngày ông được tặng một chiếc áo choàng nhung màu đỏ lộng lẫy.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhà thông thái nhìn quanh căn phòng nhỏ, thấy bàn ghế gỗ cũ nát và tấm thảm rách không còn xứng với áo choàng', 8, 'Khi khoác chiếc áo choàng quý tộc lên người, ông nhìn quanh căn phòng và thấy chiếc bàn gỗ cũ kỹ bỗng trở nên thô kệch.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Sơ đồ chuỗi phản ứng Diderot: Chiếc áo choàng đỏ -> Mua bàn làm việc mới -> Mua thảm mới -> Mua tượng đồng trang trí', 8, 'Để xứng với chiếc áo, ông gom tiền mua một chiếc bàn mới; rồi chiếc bàn mới lại đòi hỏi một tấm thảm lụa mới.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Triết gia ngồi ôm đầu giữa căn phòng tràn ngập đồ đạc xa xỉ mới mua, nhưng trong túi hoàn toàn khánh kiệt', 8, 'Chuỗi phản ứng domino mua sắm cứ thế tiếp diễn cho đến khi toàn bộ số tiền tích lũy của ông biến sạch và ông lâm vào nợ nần.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Khái niệm tài chính hiện đại: Nâng cấp một món đồ kéo theo bắt buộc nâng cấp toàn bộ hệ sinh thái xung quanh', 8, 'Trong đời sống hiện đại, hiệu ứng Diderot diễn ra hàng ngày mà bạn không hề hay biết.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật cầm chiếc điện thoại mới mua, nhìn vào củ sạc cũ và tai nghe dây cũ trên bàn', 7, 'Khi bạn mua một chiếc điện thoại cao cấp mới, bạn cảm thấy chiếc ốp lưng cũ ba mươi ngàn không còn xứng tầm.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Danh sách chi tiêu phái sinh: Điện thoại mới -> Ốp lưng hàng hiệu -> Củ sạc nhanh -> Tai nghe không dây -> Gói bảo hiểm rơi vỡ', 8, 'Bạn mua ốp lưng chính hãng năm trăm ngàn, sạc không dây một triệu, tai nghe Bluetooth ba triệu và gói bảo hiểm rơi vỡ.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật mặc bộ vest mới may rất đẹp nhưng nhìn xuống đôi giày da cũ sờn đế', 7, 'Khi bạn mua một bộ vest xịn đi làm, bạn buộc phải mua thêm một đôi giày da mới và một chiếc cặp da công sở mới.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Hiệu ứng Domino chi tiêu: Món đồ ban đầu chỉ trị giá hai mươi triệu kéo theo các khoản chi phái sinh lên đến mười lăm triệu', 8, 'Món đồ ban đầu chỉ là ngòi nổ, chính chuỗi chi tiêu đồng bộ phía sau mới là thứ tàn phá tài khoản ngân hàng của bạn.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật đứng tần ngần trước cửa hàng thời trang, cầm hóa đơn thanh toán dài dằng dặc', 7, 'Chúng ta liên tục mua sắm những thứ bổ trợ chỉ để phục vụ cho món đồ đắt tiền mà mình vừa sở hữu.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Quy tắc cảnh giác tài chính: Hãy chặn đứng hiệu ứng Diderot ngay từ mắt xích đầu tiên trước khi nó bắt đầu', 8, 'Muốn giữ được tiền, bạn phải có năng lực phát hiện và dập tắt ngòi nổ Diderot ngay từ món đồ đầu tiên.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật kiên quyết cất chiếc thẻ tín dụng vào ngăn kéo, từ chối mua thêm phụ kiện không cần thiết', 7, 'Sự hài lòng không đến từ việc đồng bộ hóa đồ đạc bên ngoài, mà đến từ sự đồng bộ giữa thu nhập và dòng tiền tích lũy.')

# --- Bẫy tâm lý 3: Thiên kiến hiện tại (Scenes 077 - 084) ---
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật ngồi nhìn chiếc bánh ngọt hấp dẫn trên đĩa, đấu tranh tâm lý giữa ăn ngay và giữ vóc dáng', 8, 'Bẫy tâm lý số ba là một cơ chế tiến hóa đã ăn sâu vào bộ não con người: Thiên kiến hiện tại hay Present Bias.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Tiêu đề đồ họa: Bẫy tâm lý số 3 - Thiên kiến hiện tại Present Bias và ảo tưởng tháng sau sẽ tiết kiệm', 8, 'Não bộ của chúng ta luôn đánh giá phần thưởng ở hiện tại cao hơn rất nhiều so với những phần thưởng tương đương trong tương lai.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật vui vẻ quẹt thẻ thanh toán bữa tiệc thịnh soạn, tự nhủ tháng sau mình sẽ thắt lưng buộc bụng', 7, 'Bạn dễ dàng tiêu hai triệu cho bữa tiệc hôm nay, và tự hứa với bản thân rằng tháng sau mình sẽ bắt đầu tiết kiệm bù lại.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Biểu đồ tâm lý học: Bản thân trong tương lai luôn bị coi như một người xa lạ phải gánh chịu hậu quả tài chính', 8, 'Các nhà nghiên cứu thần kinh học phát hiện ra: Khi nghĩ về bản thân trong mười năm tới, não bộ xử lý thông tin hệt như nghĩ về một người lạ.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Hình ảnh chiếc đồng hồ cát đang chảy, cát rơi đều đặn không dừng lại', 7, 'Bạn sẵn sàng trừng phạt bản thân của tương lai bằng cảnh rỗng ví, chỉ để đổi lấy sự thỏa mãn chốc lát của bản thân ở hiện tại.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Lời nói dối tai hại nhất: Tháng sau mình sẽ tiết kiệm là chiếc bẫy trì hoãn nguy hiểm nhất của đời người', 8, 'Thực tế chứng minh: Nếu ngày hôm nay có thêm tiền mà bạn không tiết kiệm được, thì tháng sau chắc chắn bạn cũng sẽ không làm được.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật tỉnh ngộ nhìn thẳng vào gương, nhận ra mình đã lặp lại lời hứa này suốt mười hai tháng qua', 7, 'Bởi vì khi tháng sau tới, nó lại biến thành hiện tại, và thiên kiến này sẽ tiếp tục thôi thúc bạn tiêu sạch số tiền đó.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Nguyên tắc thép: Tiết kiệm không phải là việc của tháng sau, tiết kiệm là hành động phải thực hiện ngay giây phút lương về', 8, 'Cách duy nhất để đánh bại thiên kiến hiện tại là loại bỏ hoàn toàn yếu tố ý chí ra khỏi quy trình giữ tiền.')

# --- Bảng toán Chi phí cơ hội 1 - 3 - 5 - 10 năm (Scenes 085 - 096) ---
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật mở sổ tay và máy tính tính toán lại những con số tài chính cụ thể', 7, 'Bây giờ, hãy cùng tôi làm một bài toán chi phí cơ hội thực tế để thấy cái giá bạn phải trả đắt đến mức nào.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Bảng so sánh hai kịch bản đối lập cho mười triệu tiền lương tăng thêm mỗi tháng', 8, 'Giả sử mỗi tháng bạn được tăng thêm mười triệu đồng: Kịch bản A đốt hết vào nâng cấp lối sống; Kịch bản B trích 50% đi đầu tư tích sản.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Công thức lãi kép: Năm triệu mỗi tháng, tích sản đều đặn vào chứng chỉ quỹ với lợi nhuận kỳ vọng 10% mỗi năm', 8, 'Ở kịch bản B, bạn chỉ cần giữ lại năm triệu đồng mỗi tháng, gửi đều đặn vào kênh tích sản với mức sinh lời khiêm tốn mười phần trăm một năm.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Cột mốc 1 năm: Kịch bản A có 0 đồng tích sản vs Kịch bản B có 63 triệu đồng trong tài khoản', 8, 'Sau một năm: Kịch bản A có con số không tròn trĩnh; Kịch bản B đã sở hữu sáu mươi ba triệu đồng tiền mặt an toàn.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật nhìn thấy con số sáu mươi ba triệu, đủ để chi trả toàn bộ chi phí sinh hoạt trong sáu tháng nếu có biến cố', 8, 'Số tiền sáu mươi ba triệu này chính là tấm khiên giúp bạn ngủ ngon mỗi đêm mà không phải lo sợ mất việc.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Cột mốc 3 năm: Kịch bản A vẫn 0 đồng vs Kịch bản B tích lũy được 215 triệu đồng nhờ sức mạnh lãi kép', 8, 'Sau ba năm: Trong khi người ở kịch bản A vẫn loay hoay xoay tiền trả nợ, người ở kịch bản B đã có hai trăm mười lăm triệu đồng.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Cột mốc 5 năm: Kịch bản A đối mặt với chi phí cố định khổng lồ vs Kịch bản B cán mốc 410 triệu đồng', 8, 'Sau năm năm: Con số ở kịch bản B đã tăng vọt lên bốn trăm mười triệu đồng, tương đương gần nửa tỷ đồng tích lũy.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật cầm cuốn sổ tiết kiệm và danh mục tài sản, cảm nhận được sự tự do và thanh thản thực sự', 7, 'Bốn trăm mười triệu đồng mang lại cho bạn quyền lựa chọn công việc mình yêu thích thay vì phải cắn răng làm việc vì tiền.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Cột mốc 10 năm bùng nổ: Kịch bản B chính thức vượt ngưỡng 1.1 tỷ đồng tích sản độc lập', 8, 'Và nếu kiên trì mười năm: Nhờ sức mạnh kỳ diệu của lãi kép, số tiền năm triệu mỗi tháng đã nở ra hơn một tỷ một trăm triệu đồng.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Đồ thị phân kỳ khổng lồ: Khoảng cách giữa 0 đồng và 1.1 tỷ đồng chính là cái giá của việc nâng cấp lối sống bừa bãi', 8, 'Một bên là một tỷ một trăm triệu đồng tài sản ròng; một bên là con số không kèm theo một đống đồ cũ đã lỗi thời và mất giá.')
add_s('Số liệu & Bẫy tâm lý', 'IMG', 'Nhân vật nhìn vào đồ thị tài chính với vẻ mặt chấn động và hoàn toàn thức tỉnh', 7, 'Chiếc điện thoại mới hay bữa ăn sang chảnh hôm nay không chỉ tốn vài triệu, nó đang lấy đi của bạn cả một gia tài trong tương lai.')
add_s('Số liệu & Bẫy tâm lý', 'GFX', 'Kết luận đanh thép: Tăng lương không làm bạn giàu lên, việc bạn giữ lại được bao nhiêu tiền từ khoản tăng đó mới quyết định tương lai của bạn', 8, 'Sự khác biệt giữa người giàu lên sau khi tăng lương và người nghèo đi chính là khả năng kiểm soát phần tiền tăng thêm này.')

# ==================== BEAT 4: TƯƠNG PHẢN (Scenes 097 - 120, ~180s) ====================
add_s('Tương phản', 'IMG', 'Khung hình chia đôi: Bên trái là chàng trai A sang chảnh bảnh bao, bên phải là chàng trai B giản dị điềm đạm', 8, 'Để thấy rõ sự tương phản này, hãy đặt hai đồng nghiệp cùng nhận mức lương hai mươi triệu lên bàn cân sau ba năm làm việc.')
add_s('Tương phản', 'IMG', 'Người A mặc áo vest sang trọng bước xuống từ chiếc xe tay ga đắt tiền, đeo kính râm thời thượng', 7, 'Người A chọn nâng cấp lối sống toàn diện: Anh ta chuyển sang chung cư cao cấp, đổi xe mới và thường xuyên lui tới những nơi đắt đỏ.')
add_s('Tương phản', 'IMG', 'Người B mặc áo sơ mi trắng giản dị, chạy chiếc xe máy quen thuộc, mỉm cười nhẹ nhàng bước vào văn phòng', 7, 'Người B chọn giữ nguyên mức sống cũ: Anh ta vẫn ở căn phòng vừa vặn, đi chiếc xe cũ và ăn những bữa cơm ấm áp.')
add_s('Tương phản', 'GFX', 'Bảng so sánh vẻ bề ngoài: Người A trông như một doanh nhân thành đạt; Người B trông như một nhân viên bình thường', 8, 'Nhìn từ bên ngoài, ai cũng nghĩ người A thành công hơn, kiếm được nhiều tiền hơn và có cuộc sống đáng mơ ước hơn.')
add_s('Tương phản', 'IMG', 'Người A ngồi ôm trán căng thẳng trong căn hộ chung cư lúc nửa đêm khi nhận email công ty thông báo cắt giảm nhân sự', 8, 'Nhưng bức tranh hậu trường lại hoàn toàn trái ngược: Người A sống trong nỗi sợ hãi tột cùng mỗi khi công ty có biến động.')
add_s('Tương phản', 'GFX', 'Bảng số dư thực tế của người A: Tài khoản còn đúng sáu triệu đồng, nợ thẻ tín dụng hai mươi triệu, tiền nhà đến hạn thanh toán', 8, 'Với chi phí sinh hoạt mười chín triệu mỗi tháng, người A chỉ cần chậm lương đúng mười ngày là lập tức rơi vào khủng hoảng tài chính.')
add_s('Tương phản', 'IMG', 'Người B thảnh thơi nhâm nhi tách trà bên cửa sổ, không hề có chút lo âu về những thông tin cắt giảm nhân sự', 8, 'Trong khi đó, người B sở hữu một quỹ khẩn cấp sáu tháng và một danh mục tích sản hơn hai trăm triệu đồng.')
add_s('Tương phản', 'GFX', 'Cán cân tự do tài chính: Người A có 0 ngày sống sót nếu mất việc vs Người B có 24 tháng thảnh thơi tự chủ', 8, 'Nếu mất việc, người B có thể ung dung sống hai năm mà không cần vay mượn ai một đồng nào.')
add_s('Tương phản', 'IMG', 'Người A cắn răng chịu đựng những lời mắng mỏ của sếp trong phòng họp vì không dám nghỉ việc', 7, 'Người A trở thành nô lệ cho chính mức sống của mình, không dám lên tiếng phản bác và không dám đổi việc vì áp lực nợ nần.')
add_s('Tương phản', 'IMG', 'Người B tự tin trình bày quan điểm trong cuộc họp với tâm thế vững vàng của một người tự chủ tài chính', 7, 'Người B làm việc với tâm thế tự tin, sáng tạo và thảnh thơi, bởi vì anh ta không bị đồng tiền trói buộc vào chiếc ghế làm việc.')
add_s('Tương phản', 'GFX', 'So sánh cốt lõi: Ảo giác giàu có bên ngoài vs Năng lực tài chính thực sự bên trong', 8, 'Người A chọn vẻ ngoài giàu có giả tạo; người B chọn sự tự do tài chính thực chất và bền vững.')
add_s('Tương phản', 'IMG', 'Nhân vật MC đứng trước bức tường kính thành phố, nhìn xuống dòng người tấp nập với cái nhìn thấu suốt', 8, 'Thực tế phũ phàng là: Người khác chỉ quan tâm đến những gì bạn tiêu xài trong vài giây, rồi họ sẽ quên ngay lập tức.')
add_s('Tương phản', 'GFX', 'Nghịch lý nhận thức xã hội: Người ta không ngưỡng mộ chiếc xe của bạn, họ chỉ đang tưởng tượng họ ngồi trong chiếc xe đó', 8, 'Nhà tâm lý học Morgan Housel từng viết: Không ai bị ấn tượng bởi món đồ hiệu của bạn nhiều bằng chính bản thân bạn.')
add_s('Tương phản', 'IMG', 'Nhân vật tự tin mặc chiếc áo sơ mi trắng giản dị bước đi giữa phố đông, không cần ánh nhìn công nhận của người lạ', 7, 'Khi bạn chi tiền chỉ để gây ấn tượng với người khác, bạn đang tiêu mồ hôi của mình cho những ánh nhìn vô nghĩa.')
add_s('Tương phản', 'GFX', 'Định nghĩa mới về sự giàu có: Giàu có không phải là thứ bạn khoe ra, giàu có là những gì bạn giữ lại được', 8, 'Chiếc xe bạn không mua, căn nhà bạn không nâng cấp quá đà, chính là tài sản thực sự đang bảo vệ tương lai của bạn.')
add_s('Tương phản', 'IMG', 'Nhân vật mỉm cười nhẹ nhõm khi trút bỏ được gánh nặng phải thể hiện với xã hội', 7, 'Buông bỏ được nhu cầu chứng tỏ bản thân chính là bước nhảy vọt lớn nhất trong tư duy quản lý tài chính cá nhân.')
add_s('Tương phản', 'GFX', 'Bảng tóm tắt tương phản: Lối sống hào nhoáng dẫn tới kiệt quệ vs Lối sống kỷ luật dẫn tới bình an tự tại', 8, 'Sự bình yên trong tâm hồn bắt đầu từ giây phút bạn dám sống dưới mức thu nhập của mình mà không hề cảm thấy xấu hổ.')
add_s('Tương phản', 'IMG', 'Nhân vật đặt hai bàn tay lên bàn, sẵn sàng đón nhận những giải pháp thực tế để thay đổi hoàn toàn cục diện', 8, 'Vậy làm thế nào để chúng ta vừa tận hưởng thành quả tăng lương, vừa không bị cuốn vào cỗ máy lạm phát lối sống này?')
add_s('Tương phản', 'GFX', 'Mũi tên định hướng: Từ cạm bẫy tâm lý chuyển dịch sang Hệ thống phòng thủ ba tầng thực chiến', 7, 'Câu trả lời không phải là sống kham khổ cực đoan, mà là thiết lập một hệ thống bảo vệ tự động.')
add_s('Tương phản', 'IMG', 'Master Anchor chỉ tay về phía trước, mở ra phần lộ trình hành động cụ thể từng bước', 7, 'Ngay sau đây, tôi sẽ hướng dẫn bạn quy trình ba tầng phòng thủ chi tiết để áp dụng ngay vào kỳ lương tới.')

# ==================== BEAT 5: LỘ TRÌNH 3 TẦNG PHÒNG THỦ THỰC CHIẾN (Scenes 121 - 152, ~240s) ====================
# --- Tầng 1: Đóng băng lối sống 6 tháng (Scenes 121 - 130) ---
add_s('Lộ trình giải pháp', 'GFX', 'Tiêu đề đồ họa nổi bật: Tầng phòng thủ số 1 - Quy tắc Đóng băng lối sống sáu tháng 6-Month Lifestyle Freeze', 8, 'Tầng phòng thủ đầu tiên mang tên: Quy tắc đóng băng lối sống trong sáu tháng.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật nhìn vào lịch treo tường, đánh dấu khoanh tròn cột mốc một trăm tám mươi ngày kỷ luật', 8, 'Kể từ ngày bạn nhận được email thông báo tăng lương, hãy ban hành một lệnh giới nghiêm chi tiêu cố định trong đúng một trăm tám mươi ngày.')
add_s('Lộ trình giải pháp', 'GFX', 'Biển báo ba điều cấm trong 6 tháng: 1. Cấm chuyển chỗ ở; 2. Cấm đổi xe; 3. Cấm mua đồ công nghệ đắt tiền', 8, 'Trong sáu tháng này: Tuyệt đối không chuyển nhà, không đổi xe và không mua bất kỳ món đồ công nghệ xa xỉ nào.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật kiên nhẫn lau chùi chiếc xe máy cũ và sắp xếp lại căn phòng trọ sạch sẽ ngăn nắp', 7, 'Hãy giữ nguyên mức sống cũ để cơ thể và tâm trí bạn quen dần với việc nhìn thấy một khoản tiền lớn dư ra mỗi tháng.')
add_s('Lộ trình giải pháp', 'GFX', 'Lợi ích tâm lý học: Sáu tháng giúp bộ não thoát khỏi cơn say Dopamine tăng lương và lấy lại sự tỉnh táo', 8, 'Khoảng thời gian này giúp bạn làm nguội cơn hưng phấn ban đầu, tránh được những quyết định tài chính bốc đồng không thể đảo ngược.')
add_s('Lộ trình giải pháp', 'GFX', 'Số tiền gom được sau 6 tháng: Sáu tháng nhân mười triệu bằng sáu mươi triệu đồng tiền vốn ban đầu nguyên vẹn', 8, 'Chỉ sau sáu tháng đóng băng, bạn đã tích lũy ngay được một quỹ an toàn sáu mươi triệu đồng mà không tốn một giọt mồ hôi gồng gánh.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật mỉm cười tự tin khi nhìn thấy số dư tích lũy tăng trưởng đều đặn qua từng tháng', 7, 'Cảm giác có một khoản tiền dự phòng lớn trong tay sẽ mang lại sự an tâm vượt trội hơn bất kỳ món đồ hiệu nào.')
add_s('Lộ trình giải pháp', 'GFX', 'Quy tắc vàng: Đóng băng lối sống không phải là kìm hãm, mà là tạo khoảng đệm an toàn trước khi bứt phá', 8, 'Đây là bước chạy đà cực kỳ quan trọng giúp bạn thiết lập thế chủ động hoàn toàn trước đồng tiền của chính mình.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật gật đầu kiên định, sẵn sàng chuyển sang bước tiếp theo của hệ thống', 7, 'Sau khi đã vượt qua sáu tháng thử thách, chúng ta sẽ bước sang quy tắc phân bổ dòng tiền bền vững.')
add_s('Lộ trình giải pháp', 'GFX', 'Cầu nối chuyển tiếp: Từ kỷ luật đóng băng bước sang Công thức phân bổ 50/50 thông minh', 7, 'Hết sáu tháng, bạn có được nâng cấp mức sống không? Câu trả lời là có, nhưng phải theo một tỷ lệ vàng.')

# --- Tầng 2: Quy tắc 50/50 tự động hóa (Scenes 131 - 142) ---
add_s('Lộ trình giải pháp', 'GFX', 'Tiêu đề đồ họa: Tầng phòng thủ số 2 - Quy tắc chia đôi phần lương tăng The 50/50 Increment Rule', 8, 'Tầng phòng thủ số hai chính là Quy tắc chia đôi phần lương tăng, hay công thức năm mươi năm mươi.')
add_s('Lộ trình giải pháp', 'GFX', 'Sơ đồ phân luồng 10 triệu lương tăng: 50% (5 triệu) vào Quỹ tích sản; 50% (5 triệu) nâng cấp có chủ đích', 8, 'Khi bạn được tăng thêm mười triệu đồng: Bắt buộc chia đôi số tiền này thành hai phần hoàn toàn bằng nhau.')
add_s('Lộ trình giải pháp', 'GFX', 'Nhánh số 1: Năm triệu đồng tự động chuyển vào tài khoản tích sản hoặc chứng chỉ quỹ ngay ngày nhận lương', 8, 'Năm mươi phần trăm đầu tiên, tức năm triệu đồng, phải được tự động chuyển thẳng vào tài khoản tích sản ngay ngày có lương.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật thao tác thiết lập lệnh trích tiền tự động định kỳ Auto-Debit trên ứng dụng ngân hàng số', 8, 'Hãy cài đặt lệnh trích tiền tự động vào lúc tám giờ sáng ngày nhận lương, trước khi bạn kịp nhìn thấy hoặc có ý định tiêu nó.')
add_s('Lộ trình giải pháp', 'GFX', 'Nguyên tắc trả cho mình trước: Coi năm triệu đồng này như một khoản thuế bắt buộc và chưa từng tồn tại', 8, 'Đây là nguyên tắc kinh điển: Hãy trả cho bản thân mình trước, phần còn lại mới dùng để chi trả cho cuộc sống.')
add_s('Lộ trình giải pháp', 'GFX', 'Nhánh số 2: Năm triệu đồng còn lại được phép chi tiêu nâng cấp chất lượng sống một cách hoàn toàn thoải mái', 8, 'Năm mươi phần trăm còn lại, tức năm triệu đồng, bạn được phép thoải mái dùng để nâng cấp cuộc sống của mình.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật vui vẻ đăng ký một khóa học nâng cao kỹ năng nghề nghiệp và mua giỏ thực phẩm tươi sạch hữu cơ', 8, 'Bạn có thể dùng khoản tiền này để ăn uống chất lượng hơn, đăng ký một khóa học chuyên môn hoặc phụng dưỡng cha mẹ.')
add_s('Lộ trình giải pháp', 'GFX', 'Cân bằng tâm lý: Cho phép nâng cấp 50% giúp bạn có động lực phấn đấu mà không bị ức chế tâm lý cực đoan', 8, 'Quy tắc này giúp bạn vừa tận hưởng được quả ngọt của sự thăng tiến, vừa đảm bảo tài sản tương lai vẫn sinh sôi mạnh mẽ.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật tự tin thưởng thức một bữa ăn ngon cùng người thân mà không còn cảm giác tội lỗi hay lo âu', 7, 'Bạn tiêu tiền một cách có chủ đích, tự hào và không bao giờ phải hối hận vì mình đã bảo vệ được nửa kia an toàn.')
add_s('Lộ trình giải pháp', 'GFX', 'Bảng tính lũy kế sau 3 năm áp dụng quy tắc 50/50: Vừa sống thoải mái hơn, vừa tích lũy được hơn 200 triệu đồng', 8, 'Nhờ công thức này, sau ba năm bạn vừa được nâng cấp mức sống lên hai mươi lăm phần trăm, vừa có trong tay hơn hai trăm triệu đồng.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật nhìn vào màn hình điện thoại với nụ cười hài lòng và phong thái tự tin vững vàng', 7, 'Đó chính là sự cân bằng hoàn hảo giữa hạnh phúc ở hiện tại và sự thịnh vượng ở tương lai.')
add_s('Lộ trình giải pháp', 'GFX', 'Đúc kết quy tắc 50/50: Mỗi lần tăng lương là một lần tăng gấp đôi tốc độ tự do tài chính của bạn', 8, 'Cứ mỗi nấc thang thu nhập mới, tốc độ tích sản của bạn sẽ tăng lên theo cấp số nhân thay vì trôi tuột vào chi phí.')

# --- Tầng 3: Mô hình 3 Tài khoản số & Bộ lọc vi mô (Scenes 143 - 152) ---
add_s('Lộ trình giải pháp', 'GFX', 'Tiêu đề đồ họa: Tầng phòng thủ số 3 - Hệ thống phân luồng ba tài khoản số và Bộ lọc chi tiêu 72 giờ', 8, 'Tầng phòng thủ thứ ba là thiết lập Hệ thống phân luồng ba tài khoản số và bộ lọc chi tiêu vi mô.')
add_s('Lộ trình giải pháp', 'GFX', 'Mô hình ba tài khoản ngân hàng số: 1. Tài khoản sống cơ bản; 2. Tài khoản tích sản bất khả xâm phạm; 3. Tài khoản ăn chơi có hạn mức', 8, 'Thay vì để chung toàn bộ tiền trong một tài khoản, bạn hãy mở ba tài khoản số riêng biệt trên điện thoại.')
add_s('Lộ trình giải pháp', 'GFX', 'Tài khoản số 1: Nhận lương và giữ nguyên mười triệu cho toàn bộ chi phí sinh hoạt thiết yếu', 8, 'Tài khoản một giữ nguyên mười triệu cho chi phí sinh hoạt căn bản: tiền nhà, tiền ăn, hóa đơn điện nước.')
add_s('Lộ trình giải pháp', 'GFX', 'Tài khoản số 2: Tích sản năm triệu tự động chuyển đi đầu tư, không cài app chuyển tiền trên máy để tránh rút bừa', 8, 'Tài khoản hai là két sắt tích sản năm triệu: Tiền chỉ có một chiều đi vào, tuyệt đối không gắn thẻ ATM chi tiêu.')
add_s('Lộ trình giải pháp', 'GFX', 'Tài khoản số 3: Năm triệu cho giải trí và nâng cấp, quẹt hết là dừng lại, không được phép bù trừ', 8, 'Tài khoản ba là tài khoản trải nghiệm năm triệu: Bạn được quyền tiêu sạch khoản này cho sở thích mà không cần áy náy.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật dừng tay trước nút bấm Mua ngay trên sàn thương mại điện tử, đặt điện thoại xuống bàn', 8, 'Đi kèm với hệ thống tài khoản là Quy tắc bảy mươi hai giờ: Trước mọi quyết định mua đồ ngoài danh mục, hãy chờ đủ ba ngày.')
add_s('Lộ trình giải pháp', 'GFX', 'Đồng hồ đếm ngược 72 giờ: 80% ham muốn mua sắm bốc đồng sẽ tự động biến mất sau ba ngày suy nghĩ', 8, 'Sau bảy mươi hai giờ, cơn sốt Dopamine sẽ hạ nhiệt; tám mươi phần trăm trường hợp bạn sẽ nhận ra mình không hề cần món đồ đó.')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật cầm chiếc máy tính mini, quy đổi giá tiền chiếc áo hai triệu thành hai mươi giờ làm việc', 7, 'Bộ lọc thứ hai là Quy đổi giá trị ra giờ lao động: Lấy giá món đồ chia cho thu nhập mỗi giờ làm việc của bạn.')
add_s('Lộ trình giải pháp', 'GFX', 'Công thức quy đổi thực tế: Thu nhập 100 ngàn/giờ -> Chiếc đồng hồ 6 triệu tương đương 60 giờ cày cuốc', 8, 'Nếu bạn kiếm được một trăm ngàn một giờ, chiếc đồng hồ sáu triệu đồng tương đương sáu mươi giờ làm việc vất vả, liệu có xứng đáng?')
add_s('Lộ trình giải pháp', 'IMG', 'Nhân vật mỉm cười thanh thản, tự tin làm chủ hoàn toàn mọi quyết định chi tiêu hàng ngày', 7, 'Khi bạn nhìn món đồ dưới góc độ thời gian của cuộc đời mình, bạn sẽ trở thành một người tiêu dùng cực kỳ thông thái.')
add_s('Lộ trình giải pháp', 'GFX', 'Hệ thống hoàn chỉnh: Ba tầng phòng thủ kết hợp tạo thành bức tường thành vững chắc bảo vệ tương lai của bạn', 8, 'Ba tầng phòng thủ này không hề tốn thời gian, nhưng nó sẽ bảo vệ bạn trọn đời trước mọi cám dỗ của lạm phát lối sống.')

# ==================== BEAT 6: KẾT BÌNH YÊN (Scenes 153 - 160, ~60s) ====================
add_s('Kết bình yên', 'GFX', 'Cây tài sản xanh tươi đâm chồi nảy lộc, tỏa bóng mát che chở cho ngôi nhà nhỏ ấm cúng', 8, 'Tài chính cá nhân không phải là cuộc đua xem ai tiêu xài hoành tráng hơn hay ai đổi điện thoại nhanh hơn.')
add_s('Kết bình yên', 'IMG', 'Nam MC đại diện kênh ngồi đọc sách bên hiên nhà ngập tràn ánh nắng ấm áp, tâm thái an nhiên', 7, 'Nó là hành trình xây dựng sự bình yên nội tại, nơi bạn không còn phải giật mình thon thót mỗi khi nhận thông báo số dư.')
add_s('Kết bình yên', 'GFX', 'Sơ đồ tự do đích thực: Kiếm tiền thông minh -> Giữ tiền kỷ luật -> Tự do lựa chọn cuộc sống', 8, 'Sự giàu có thực sự là quyền được tự do lựa chọn công việc mình yêu thích và có thể nói không với những điều mình không muốn.')
add_s('Kết bình yên', 'GFX', 'Câu quote tâm đắc dập nổi: Tài sản lớn nhất của một con người không phải là đồ hiệu, mà là sự tự do trong tâm trí', 8, 'Hãy để mỗi đồng tiền tăng thêm trở thành một viên gạch xây dựng tự do, thay vì trở thành sợi dây xích trói buộc bạn.')
add_s('Kết bình yên', 'AIV', 'Chàng trai văn phòng 27 tuổi mặc sơ mi trắng tự tin sải bước trên con phố nhộn nhịp với nụ cười thanh thản và ánh mắt rạng ngời', 6, 'Từ kỳ lương tới, hãy áp dụng công thức năm mươi năm mươi để làm chủ dòng tiền.')
add_s('Kết bình yên', 'AIV', 'Chàng trai đứng trên đỉnh đồi lộng gió lúc bình minh, hít thở bầu không khí trong lành, ánh mặt trời vàng ấm áp chiếu rọi', 6, 'Bạn xứng đáng có sự thảnh thơi tài chính, tạo nên bởi chính kỷ luật của mình.')
add_s('Kết bình yên', 'GFX', 'Logo Tiền Thực Chiến hiện lên trang nhã cùng slogan: Kiến thức thực chiến - Hành động mỗi ngày - Bình an tài chính', 8, 'Nếu thấy video này hữu ích, hãy nhấn Đăng ký kênh Tiền Thực Chiến để cùng nhau xây dựng nền tảng tài chính vững vàng.')
add_s('Kết bình yên', 'IMG', 'Master Anchor mỉm cười ấm áp giơ tay chào tạm biệt khán giả trong khung hình tinh tế', 8, 'Tôi là người đồng hành của bạn tại Tiền Thực Chiến. Cảm ơn bạn đã lắng nghe và hẹn gặp lại ở video tiếp theo.')

# Write to script.md
lines = []
lines.append('# Script — lam-phat-loi-song-luong-tang-tien-mat')
lines.append('Kênh: Tiền Thực Chiến | Ngôn ngữ: vi | Mục tiêu: 20 phút | TTS: vieneu | Voice: Hải Đăng')
lines.append('')

total_words = 0
total_dur = 0
aiv_count = 0
gfx_count = 0
img_count = 0

for s in scenes:
    words = len(s['nar'].split())
    total_words += words
    total_dur += s['dur']
    if s['type'] == 'AIV':
        aiv_count += 1
    elif s['type'] == 'GFX':
        gfx_count += 1
    elif s['type'] == 'IMG':
        img_count += 1

    lines.append(f'## Scene {s["num"]:03d}')
    lines.append(f'- Beat: {s["beat"]}')
    lines.append(f'- Loại dự kiến: {s["type"]}')
    lines.append(f'- Visual concept: {s["concept"]}')
    lines.append(f'- Duration ước tính: {s["dur"]}s')
    lines.append(f'- Narration: "{s["nar"]}"')
    lines.append('')

script_path.parent.mkdir(parents=True, exist_ok=True)
script_path.write_text('\n'.join(lines), encoding='utf-8')

print(f'✅ Successfully generated {len(scenes)} scenes!')
print(f'⏱️ Total estimated duration: {total_dur}s ({total_dur/60:.2f} mins)')
print(f'📝 Total words: {total_words} words (Average pace: {total_words/total_dur:.2f} words/sec)')
print(f'🎨 Asset breakdown: AIV: {aiv_count}, GFX: {gfx_count}, IMG: {img_count}')
