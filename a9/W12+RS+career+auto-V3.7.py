# 添加get_new_progress进度函数（固定代码勿动）
import re

from .core.ocr import OCR

logger.info("add get_new_progress")

@classmethod
def get_new_progress(cls, image_path=None, capture=False):
    """识别计时赛进度"""
    for _ in range(2):
        text = cls._get_text(
            crop=(155, 82, 373, 130), replace=True, config="--psm 11"
        )
        pattern = r"\b\d{1,3}\b"
        match = re.search(pattern, text)
        if match and "%" in text:
            m = match.group()
            if int(m) > 100:
                num = int(m[:2])
            else:
                num = int(m)
            return num
    return -1

OCR.get_new_progress = get_new_progress

logger.info("add get_new_progress over")

# 添加get_time_progress计时赛进度函数（固定代码勿动）
import re

from .core.ocr import OCR

logger.info("add get_time_progress")

@classmethod
def get_time_progress(cls, image_path=None, capture=False):
    """识别计时赛进度"""
    for _ in range(2):
        text = cls._get_text(
            crop=(155, 27, 373, 75), replace=True, config="--psm 11"
        )
        pattern = r"\b\d{1,3}\b"
        match = re.search(pattern, text)
        if match and "%" in text:
            m = match.group()
            if int(m) > 100:
                num = int(m[:2])
            else:
                num = int(m)
            return num
    return -1

OCR.get_time_progress = get_time_progress

logger.info("add get_time_progress over")

# 自定义循环指令开始
# 蓝币买票、买油（补油）开关
REFILL_TICKETS = 0 # 蓝币买票开关（0-不使用蓝币买票，1-使用蓝币买票，2-使用蓝币补票），注意只有车辆有油的情况会使用蓝币补票，启用补票后每次循环开始仅特定次数自动买票，去除回票时间差，循环次数对应设置成车辆油量
REFILL_TICKETS_POSITION = 0 # 蓝币补票位置（对应数值修改成需要第几次补充票数），注意只有蓝币补票开关开启的情况有效，只有车辆有油的情况会使用蓝币补票
REFILL_GAS = 0 # 蓝币买油开关（0-不使用蓝币买油，1-使用蓝币买油，2-使用蓝币补油），注意只有主车辆会使用蓝币买油，启用补油后每次循环开始仅第一次自动补充燃油，去除回油时间差，循环次数对应设置成车辆油量

# 循环次数、生涯设置、auto设置、BBYY设置、重启设置
sr_keyword = 'W12' # showroom自定义关键字
sr_stages = [3] # showroom执行XXXX阶段，[1]表示仅执行1阶段，[1,2]表示执行1和2阶段，依此类推，目前只能执行1,2,3,4,5,6,7,8,9,10,11,12阶段，设置为0为不执行
sr_times = 3 # showroom每阶段执行XXXX次，设置为0为不执行
sh_keyword = 'ULT' # specialhunt自定义关键字
sh_position = 1 # specialhunt位置
sh_stages = [6] # specialhunt执行XXXX阶段，[1]表示仅执行1阶段，[1,2]表示执行1和2阶段，依此类推，目前只能执行1,2,3,4,5,6阶段，设置为0为不执行
sh_times = 12 # specialhunt每阶段执行XXXX次，设置为0为不执行
hunt_take_up_time = 1 # 特赛寻车/寻车是否计入生涯/auto时间（0-不计入生涯/auto时间，1-若只开启生涯计入生涯时间，若同时开启生涯/auto计入生涯时间，若只开启auto计入auto时间）
career_time = 0 # 生涯运行XXXX分钟，设置为0为不启动生涯
career_select = 1 # 生涯选择（0-第四章 Euro Show Down 12永恒之城，1-第六章 British Tour 4紫色大道）
career0_car = [[1, 11], [1, 16], [1, 18], [2, 19]] # 生涯0选车，每一车需要用[x, y]括起来，x是行，y是列，绝对位置即可
career1_car = [[2, 4], [1, 5], [1, 7], [1, 8], [1, 9], [2, 10]] # 生涯1选车，每一车需要用[x, y]括起来，x是行，y是列，绝对位置即可
free_pack = 1 # 生涯是否自动领卡（0-关闭自动领卡，1-开启自动领卡）
target_page = 3 # 结束后目标页面（0-不操作，1-每日活动，2-多人游戏，3-多人1，4-多人2）根据auto任务设置可节省定位时间
auto_time = 61 # auto运行XXXX分钟，设置为0为不启动auto
auto_stop = 2 # auto停止方式（0-70%比赛进度停止，1-NEXT按钮停止，2-3分钟强制停止）
enable_BBYY = 0 # BBYY开关（0-关闭BBYY，1-开启BBYY）
Operation_progress = 80 # BBYY操作进度设置
BBYY_pos = 4 # BBYY排名设置，为第X及更低名次执行BB操作
enable_restart = 1 # 重启开关（0-关闭重启，1-循环结束后重启）

#（ 固定代码勿动）
REFILL_TICKETS_POSITION = REFILL_TICKETS_POSITION - 1

# showroom阶段设置检查
if not set(sr_stages).issubset(set([1,2,3,4,5,6,7,8,9,10,11,12])):
    sr_times = 0
    logger.info("showroom重新检查阶段，目前仅能执行阶段1,2,3,4,5,6,7,8,9,10,11,12")

for srstage in sr_stages:

    # 自定义寻路文件
    if srstage == 1:
        LL = []
        L = [6,7,8,52,53,54,67,68,69,78,79,80]
        RR = []
        R = [13,14,15,28,29,30]
        B = ["4-2.5","5-1.5","12-2","13-1","17-3","18-2","23-2","24-1","33-1","36-3.5","43-2","62-1","69-2","70-1","84-3","91-1.5","95-2.5","96-1.5"]
        BB = []
        YY_1 = []#蓝喷
        YY_2 = [8,9,10,15,16,17,26,27,41,42,47,48,49,50,51,55,56,64,65,81,82,88,89,94,98,99]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 2:
        LL = []
        L = [14,15,16,79,80]
        RR = []
        R = [5,6,7,30,31,56,57,64,65,66]
        B = ["17-2","18-1.5","26-0.1","32-3.5","33-3","45-0.1""47-3","48-2.5","67-3","68-2.5"]
        BB = []
        YY_1 = [27,28,41,42,75,76,82,83]#蓝喷
        YY_2 = [23,24,25,57,58,59,90,91,92,93,94,95,96,97,98]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 3:
        LL = []
        L = [21,22,33,34,35,52,53,54,75,76]
        RR = []
        R = [57,58,59,64,65,80,81]
        B = ["17-3","18-2","31-1.5","32-0.5","45-3","46-2","70-2","85-3"]
        BB = [15,16,40,41,44]
        YY_1 = [4,20,25,26,27,28,36,37,48,49,50,67,72,73,74]#蓝喷
        YY_2 = [42,62,63,82,83,89,90,91,94,95,96]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            if progress == 0:
               time.sleep(3.7)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               #time.sleep(0.3)
               #pro.press('B')
               #time.sleep(0.1)
               #pro.release('B')
            if progress == 8:
               pro.press('B')
               time.sleep(5.5)
               pro.press_button("DPAD_LEFT", 0)
               pro.press('B')
               time.sleep(0.5)
               pro.release('B')
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
            if progress == 58:
               pro.press('B')
               time.sleep(0.5)
               pro.press_button("DPAD_RIGHT", 0)
               pro.press('B')
               time.sleep(3.5)
               pro.release('B')
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.8)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
            if progress == 79:
               pro.press('B')
               time.sleep(0.2)
               pro.press_button("DPAD_RIGHT", 0)
               pro.press('B')
               time.sleep(3)
               pro.release('B')
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
            if progress == 92:
               pro.press('B')
               time.sleep(0.5)
               pro.press_button("DPAD_RIGHT", 0)
               pro.press('B')
               time.sleep(1)
               pro.release('B')
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
            
    if srstage == 4:
        LL = []
        L = [13,14,53]
        RR = []
        R = [0,1,3,4,8,9,10,69,70,81,82]
        B = ["4-4","5-3","10-2","11-1","17-0.1","31-3.5","32-3","50-3","51-2","66-3","67-2","80-0.5","82-3","83-2","86-4.5","87-3.5"]
        BB = [21,22,36,37,56,57]
        YY_1 = [12,13,20,21,38,39]#蓝喷
        YY_2 = [8,9,14,15,23,31,32,54,55,58,59,72,73,85,86,91,92,95,96,97]#紫喷
        REPEAT_1 = [0,1]#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 5:
        LL = [58,59,60]
        L = [18,19,20,32,33,54,55,64,65,74,75,76]
        RR = []
        R = [81,82,83]
        B = ["5-5.5","6-5","22-0.1","25-2","26-1.5","36-0.1","47-2.5","48-2","63-0.1","66-2.5","67-2","78-0.1","85-0.1"]
        BB = []
        YY_1 = [16,17,38,39,56,57,86,87]#蓝喷
        YY_2 = [34,35,76,77,80]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 6:
        LL = []
        L = [28,29,51,52]
        RR = [43,44]
        R = [3,4,5,15,16,21,22,23,24,65,66,67]
        B = ["9-2","10-1.5","31-1.5","35-1.5","57-2.5","58-1.5","85-2","86-1"]
        BB = [93,94]
        YY_1 = [8,78,79]#蓝喷
        YY_2 = [17,18,25,26,39,40,48,49,64,89,90,95,96,97]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 7:
        LL = [82,83]
        L = [48,49,53,54,55,56]
        RR = []
        R = [11,12,13,20,21,22,23,24,32,33,42,43,44]
        B = ["3-1.5","4-1","17-2","18-1","22-0.1","24-3","25-2.5","34-1.5","35-0.5","41-0.1","50-0.1","62-5","63-4.5","73-3.5","74-2.5","83-4","84-3"]
        BB = []
        YY_1 = [51,52]#蓝喷
        YY_2 = [3,5,6,8,9,21,30,31,37,38,47,48,71,72,80,81,91,92,95,96,97,98]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 8:
        LL = []
        L = [20,21,24,25,48,49]
        RR = [69,70]
        R = [7,8,9,52,53,57,58]
        B = ["4-3","5-2","15-2","16-1","38-4","39-3","40-2","59-1.5","60-0.5","65-2","66-1"]
        BB = [26,27]
        YY_1 = [35,36,80,81,84,85,90,91]#蓝喷
        YY_2 = [18,19,22,23,28,29,43,44,54,55,56,59,60,64,65,67,68,71,72,73,94,95,97,98]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 9:
        LL = []
        L = [27,28,29,34,35,43,44]
        RR = []
        R = [5,6,7,63,64]
        B = ["14-2.5","15-2","22-2","23-1.5","56-3","57-2.5","68-3","69-2.5"]
        BB = [49,50,87,88]
        YY_1 = [26,27,32,33,41,42,83,84]#蓝喷
        YY_2 = [18,19,53,54,61,62,64,65,74,75,94,95,96]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 10:
        LL = []
        L = [2,3]
        RR = []
        R = [21,22,47,48,68,69,77,78,79,80,81,82,83]
        B = ["8-8","34-3","59-3.5","77-3","92-2"]
        BB = []
        YY_1 = [40,41,47,50,53,55,96,97]#蓝喷
        YY_2 = [3,22,47,48,69,70,71,84,85]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 11:
        LL = [6,7,8]
        L = [10,11,12,13,16,17,18,59,60,61,64,65,66]
        RR = []
        R = [2,3,4,27,28,29,39,40,41,44,45,46]
        B = ["13-3","18-0.1","26-4","31-0.1","34-5","41-0.1","49-3","61-4","76-1","82-1","91-1.5","95-1.5",]
        BB = []
        YY_1 = [19,20,33,34,42,43,50,51,84,85]#蓝喷
        YY_2 = [17,18,30,31,40,41,47,48,56,57,68,69,78,79,94,97,98]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if srstage == 12:
        LL = []
        L = [3,4,5,14,15,16,18,19,20,23,24,31,32,44,74,75,]
        RR = []
        R = [79,83,84,88]
        B = ["6-1.5","9-4.5","23-2","25-1.5","38-2","54-3.1","64-0.1","66-4.5","71-1.5","90-4","96-2"]
        BB = [27,28,50,51,60,61,77,80,81,85,86]
        YY_1 = [13]#蓝喷
        YY_2 = [7,8,17,21,22,29,30,33,40,41,42,52,62,63,70,76,78,82,87,94,95,97,98,99]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    # 复位到生涯页面（固定代码勿动）
    if sr_times != 0:
        for show_room in range(1000):
            for index in range(4):
                pro.press_group(['B'] * 5, 1)
                page = OCR.get_page()
                logger.info(f"page name = {page.name}")
                if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                   logger.info(f"main menu")
                   break
            time.sleep(2)
            pro.press_group(['DPAD_DOWN'] * 5, 0.1)
            pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
            pro.press_group(['A'], 2)
            pro.press_group(['B'] * 2, 1)

    # 从生涯定位到自定义目标页面
            pro.press_group(['ZL'] * 3, 1)
            for index in range(20):
                time.sleep(0.5)
                page = OCR.get_page()
                logger.info(f"page name = {page.name}")
                if sr_keyword in page.text:
                    break
            if sr_keyword in page.text:
                pro.press_button('A', 0) 
                for index in range(20):
                    time.sleep(0.5)
                    page = OCR.get_page()
                    logger.info(f"page name = {page.name}")
                    if "HELP" in page.text:
                        break
                if "HELP" in page.text:
                    pro.press_group(['DPAD_LEFT'] * 15, 0)
                    time.sleep(0.5)
                    pro.press_group(['DPAD_RIGHT'] * srstage, 0.5)
                    time.sleep(0.5)
                    pro.press_button('A', 0)
                    break

    # （固定代码勿动）
    if sr_times != 0:
        B = {int(item.split('-')[0]): float(item.split('-')[1]) for item in B}

    for race_times in range(sr_times):# 循环X次
        logger.info(f"Stage = {srstage}；Starts/sr_times = {race_times + 1} / {sr_times}；WaitingTime = {career_time + auto_time} minutes")
    # 从比赛详情页进入至车辆详情
        time.sleep(3)
        pro.press_button('A', 0)
        for index in range(4):
            time.sleep(0.5)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")
            if page.name == "car_info":
                break
        if page.name != "car_info":
            pro.press_button('A', 0)
            time.sleep(2)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")

    # 检测play按钮是否有效（固定代码勿动）
        for index in range(3):
            time.sleep(2)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")
            mode = consts.car_hunt_zh
            states_a = OCR.has_play(mode)
            logger.info(f"states_a = {states_a}")
            mode = consts.legendary_hunt_zh
            states_b = OCR.has_play(mode)
            logger.info(f"states_b = {states_b}")
            mode = consts.custom_event_zh
            states_c = OCR.has_play(mode)
            logger.info(f"states_c = {states_c}")
            if states_a or states_b or states_c or page.name == "searching" or page.name == "loading_race" or page.name == "racing":
                break
        if states_a or states_b or states_c or page.name == "searching" or page.name == "loading_race" or page.name == "racing":
    # 检测页面蓝币补票开关（固定代码勿动）
           if REFILL_TICKETS == 2 and race_times == REFILL_TICKETS_POSITION:
              pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_UP','DPAD_UP','DPAD_UP','DPAD_UP','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT'], 0.2)
              time.sleep(2)
              pro.press_group(['DPAD_DOWN','A','A','DPAD_DOWN','A','B','B','A','A'], 2)
           else:
              pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','A'], 0.2)
    # 检测页面蓝币补票开关结束（固定代码勿动）
           time.sleep(3)
           page = OCR.get_page()
           logger.info(f"page name = {page.name}")
           if page.name == "car_info":
              time.sleep(2)
              page = OCR.get_page()
              logger.info(f"page name = {page.name}")
              mode = consts.car_hunt_zh
              states_a = OCR.has_play(mode)
              logger.info(f"states_a = {states_a}")
              mode = consts.legendary_hunt_zh
              states_b = OCR.has_play(mode)
              logger.info(f"states_b = {states_b}")
              mode = consts.custom_event_zh
              states_c = OCR.has_play(mode)
              logger.info(f"states_c = {states_c}")
              if states_a or states_b or states_c:
                 pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','A'], 0.2)
                 time.sleep(3)
                 page = OCR.get_page()
                 logger.info(f"page name = {page.name}")
                 if page.name == "car_info" or page.name == "switch_home":
                    break
              else:
                 break
        else:
            break

    # 检测whether reward is complete
        if ("AGAI" in page.text):
           pro.press_group(['A'], 1)
           break

    # 检测页面蓝币买票开关（固定代码勿动）
        if (page.name == "tickets" or "REFILL" in page.text or "refill" in page.text) and REFILL_TICKETS == 0: # refill for gas, watch the capital is for the ticket
           break
        elif (page.name == "tickets" or "REFILL"  in page.text) and REFILL_TICKETS == 1:
           pro.press_group(['A', 'DPAD_DOWN', 'A', 'B', 'A', 'A'], 2)

    # 寻路文件按进度执行（固定代码勿动）
        completed = []
        index_a = 0
        index_b = 0
        index_c = 0
        for index in range(1000):
            progress = OCR.get_progress()
            logger.info(f"progress = {progress}")
            if progress == -1:
               index_c = index_b + 1
               index_b = index_a + 1
               index_a = index
               if index_a == index_b and index_b == index_c:
                  has_next = OCR.has_next()
                  logger.info(f"has_next = {has_next}")
                  if has_next:
                     break
            if progress in completed:
               continue

    # 特殊进度优先部分开始（固定代码勿动）
            special_progress(progress)

    # 特殊进度优先部分结束（固定代码勿动）
            if progress in LL:
               pro.press_group(['DPAD_LEFT'] * 2, 0.1)
            if progress in L:
               pro.press_button("DPAD_LEFT", 0)
            if progress in RR:
               pro.press_group(['DPAD_RIGHT'] * 2, 0.1)
            if progress in R:
               pro.press_button("DPAD_RIGHT", 0)
            if progress in B:
               duration = B.get(progress)
               pro.press_buttons("B", down=duration)
            if progress in BB:
               pro.press('B')
               time.sleep(0.1)
               pro.release('B')
               time.sleep(0.1)
               pro.press('B')
               time.sleep(0.1)
               pro.release('B')
               time.sleep(0.1)
               pro.press('B')
               time.sleep(0.1)
               pro.release('B')
            if progress in YY_1:
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.8)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
            if progress in YY_2:
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
            if progress not in REPEAT_1:
               completed.append(progress)

    # 强制复位比赛详情页
        pro.press_group(['B'] * 2, 0.2)
        time.sleep(1)
        for index in range(15):
            time.sleep(0.2)
            has_next = OCR.has_next()
            logger.info(f"has_next = {has_next}")
            if has_next:
                pro.press_group(['B'] * 1, 0.2)
                break
        for index in range(20):
            has_next = OCR.has_next()
            logger.info(f"has_next = {has_next}")
            if has_next:
                pro.press_group(['B'] * 1, 0.2)
            else:
                break
        time.sleep(8)
        pro.press_button('B', 0) # no reward, so no need of so many  B
        time.sleep(3)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if page.name == "star_up":
           pro.press_button('B', 0)

# specialhunt阶段设置检查
if not set(sh_stages).issubset(set([1,2,3,4,5,6])):
    sh_times = 0
    logger.info("specialhunt重新检查阶段，目前仅能执行阶段1,2,3,4,5,6")

specialhunt_start_time = time.time()
for shstage in sh_stages:

    # 自定义寻路文件
    if shstage == 1:
        LL = []
        L = [2,3,4,44,45,46,47,52,53,54,62,63,64]
        RR = []
        R = [21,22,23]
        B = ["16-2","17-1.5","35-1.5","36-1","41-1","42-0.5","54-2.5","55-2","71-2","72-1.5"]
        BB = [77,78,85,86,87]
        YY_1 = [54,55]#蓝喷
        YY_2 = [4,5,6,7,8,9,27,28,30,31,35,36,47,48,49,71,72,74,75,80,81,82,88,89,90,91]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if shstage == 2:
        LL = []
        L = [17,18,43,44]#16,17
        RR = []
        R = []#25,26,33,34
        B = ["25-6","26-5.5","53-1","54-0.5","61-2","62-1.5","72-3.5","73-3","85-3","86-2.5"]#"12-0.1","17-1","18-0.5","25-2.5","26-2","34-1.2","35-0.7","62-2","63-2.5","72-3.5","73-3","85-3","86-2.5"
        BB = [45,46]
        YY_1 = []#蓝喷23,24
        YY_2 = [10,11,23,39,40,47,48,57,58,65,66,68,80,81,93,94,95]#紫喷10,11,34,36,37,38,39,40,53,54,62,63,72,73,85,86,95,96,97
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if shstage == 3:
        LL = []
        L = []
        RR = []
        R = [14,15,16]
        B = ["16-2","17-1.5","31-3","32-2.5","64-9","65-8.5"]
        BB = []
        YY_1 = []#蓝喷12,13
        YY_2 = [24,25,26,40,41,89,90,91]#紫喷23,24,41,42,43,47,48,56,57,76,77,78,86,87,88
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if shstage == 4:
        LL = []
        L = [15,16,17,69,70]
        RR = []
        R = [25,26,27,53,54]
        B = ["10-1.5","11-1","18-1","19-0.5","39-4","40-3.5","70-2","71-1.5"]
        BB = []
        YY_1 = []#蓝喷
        YY_2 = [13,14,23,24,25,26,27,55,56,57,75,76,94,95,96]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if shstage == 5:
        LL = []
        L = [14,15,16]
        RR = []
        R = [0,1,2,3,4,5,6,7,8,9]
        B = ["35-21","36-20","37-20"]
        BB = []
        YY_1 = [11,12,16,17,18]#蓝喷
        YY_2 = [85,86,87,88,89,90,91,92,93,94,95,96,97,98,99]#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if shstage == 6:
        LL = []
        L = []
        RR = []
        R = [27,28]#27,28,59,60,61
        B = ["14-0.5","35-6.5","36-6","73-4","74-3.5","85-3","86-2.5","94-1","95-0.5"]#"14-0.5","46-0.8","73-4","86-2.2"
        BB = []
        YY_1 = [25,26,29,67]#蓝喷21,29,32,67
        YY_2 = [10,18,48,49,50,51,52,64,65,83,91,92,95,96,97]#紫喷10,18,25,26,50,51,52,83,84,91
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
            
    if shstage == 7:
        LL = []
        L = []
        RR = []
        R = []
        B = []
        BB = []
        YY_1 = []#蓝喷
        YY_2 = []#紫喷
        REPEAT_1 = []#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机
        def special_progress(progress):
            """特殊进度优先部分"""
            pass
           
    # 复位到特赛页面（固定代码勿动）
    if sh_times != 0:
        for special_hunt in range(1000):
            for index in range(4):
                pro.press_group(['B'] * 5, 1)
                page = OCR.get_page()
                logger.info(f"page name = {page.name}")
                if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                   logger.info(f"main menu")
                   break
            time.sleep(2)
            pro.press_group(['ZR'] * 1, 1)
            pro.press_group(['DPAD_DOWN'] * 10, 0.1)
            pro.press_group(['DPAD_LEFT'] * 7, 0.1)
            pro.press_group(['DPAD_RIGHT'] * 1, 0.1)
            pro.press_group(['A'], 2)

    # 从特赛定位到自定义目标页面
            pro.press_group(['DPAD_UP'] * 7, 0.2)
            pro.press_group(['DPAD_DOWN'] * sh_position, 0.2)
            pro.press_group(['A'], 2)
            pro.press_group(['B'], 2)
            for index in range(20):
                time.sleep(0.5)
                page = OCR.get_page()
                logger.info(f"page name = {page.name}")
                if sh_keyword in page.text:
                    break
            if sh_keyword in page.text:
                pro.press_button('A', 0) 
                for index in range(20):
                    time.sleep(0.5)
                    page = OCR.get_page()
                    logger.info(f"page name = {page.name}")
                    if "HELP" in page.text:
                        break
                if "HELP" in page.text:
                    pro.press_group(['DPAD_LEFT'] * 9, 0)
                    time.sleep(0.5)
                    pro.press_group(['DPAD_RIGHT'] * shstage, 0.5)
                    time.sleep(0.5)
                    pro.press_button('A', 0)
                    break

    # （固定代码勿动）
    if sh_times != 0:
        B = {int(item.split('-')[0]): float(item.split('-')[1]) for item in B}

    for race_times in range(sh_times):# 循环X次
        logger.info(f"Stage = {shstage}；Starts/sh_times = {race_times + 1} / {sh_times}；WaitingTime = {career_time + auto_time} minutes")
    # 从比赛详情页进入至车辆详情
        time.sleep(3)
        pro.press_button('A', 0)
        for index in range(4):
            time.sleep(0.5)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")
            if page.name == "car_info":
                break
        if page.name != "car_info":
            pro.press_button('A', 0)
            time.sleep(2)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")

    # 检测play按钮是否有效（固定代码勿动）
        for index in range(3):
            time.sleep(2)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")
            mode = consts.car_hunt_zh
            states_a = OCR.has_play(mode)
            logger.info(f"states_a = {states_a}")
            mode = consts.legendary_hunt_zh
            states_b = OCR.has_play(mode)
            logger.info(f"states_b = {states_b}")
            mode = consts.custom_event_zh
            states_c = OCR.has_play(mode)
            logger.info(f"states_c = {states_c}")
            if states_a or states_b or states_c or page.name == "searching" or page.name == "loading_race" or page.name == "racing":
                break
        if states_a or states_b or states_c or page.name == "searching" or page.name == "loading_race" or page.name == "racing":
    # 检测页面蓝币补票开关（固定代码勿动）
           if REFILL_TICKETS == 2 and race_times == REFILL_TICKETS_POSITION:
              pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_UP','DPAD_UP','DPAD_UP','DPAD_UP','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT'], 0.2)
              time.sleep(2)
              pro.press_group(['DPAD_DOWN','A','A','DPAD_DOWN','A','B','B','A','A'], 2)
           else:
              pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','A'], 0.2)
    # 检测页面蓝币补票开关结束（固定代码勿动）
           time.sleep(3)
           page = OCR.get_page()
           logger.info(f"page name = {page.name}")
           if page.name == "car_info":
              time.sleep(2)
              page = OCR.get_page()
              logger.info(f"page name = {page.name}")
              mode = consts.car_hunt_zh
              states_a = OCR.has_play(mode)
              logger.info(f"states_a = {states_a}")
              mode = consts.legendary_hunt_zh
              states_b = OCR.has_play(mode)
              logger.info(f"states_b = {states_b}")
              mode = consts.custom_event_zh
              states_c = OCR.has_play(mode)
              logger.info(f"states_c = {states_c}")
              if states_a or states_b or states_c:
                 pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','A'], 0.2)
                 time.sleep(3)
                 page = OCR.get_page()
                 logger.info(f"page name = {page.name}")
                 if page.name == "car_info" or page.name == "switch_home":
                    break
              else:
                 break
        else:
            break

    # 检测whether reward is complete
        if ("AGAI" in page.text):
           pro.press_group(['A'], 1)
           break

    # 检测页面蓝币买票开关（固定代码勿动）
        if (page.name == "tickets" or "REFILL" in page.text or "refill" in page.text) and REFILL_TICKETS == 0: # refill for gas, watch the capital is for the ticket
           break
        elif (page.name == "tickets" or "REFILL"  in page.text) and REFILL_TICKETS == 1:
           pro.press_group(['A', 'DPAD_DOWN', 'A', 'B', 'A', 'A'], 2)

    # 寻路文件按进度执行（固定代码勿动）
        completed = []
        index_a = 0
        index_b = 0
        index_c = 0
        for index in range(1000):
            progress = OCR.get_progress()
            logger.info(f"progress = {progress}")
            if progress == -1:
               index_c = index_b + 1
               index_b = index_a + 1
               index_a = index
               if index_a == index_b and index_b == index_c:
                  has_next = OCR.has_next()
                  logger.info(f"has_next = {has_next}")
                  if has_next:
                     break
            if progress in completed:
               continue

    # 特殊进度优先部分开始（固定代码勿动）
            special_progress(progress)

    # 特殊进度优先部分结束（固定代码勿动）
            if progress in LL:
               pro.press_group(['DPAD_LEFT'] * 2, 0.1)
            if progress in L:
               pro.press_button("DPAD_LEFT", 0)
            if progress in RR:
               pro.press_group(['DPAD_RIGHT'] * 2, 0.1)
            if progress in R:
               pro.press_button("DPAD_RIGHT", 0)
            if progress in B:
               duration = B.get(progress)
               pro.press_buttons("B", down=duration)
            if progress in BB:
               pro.press('B')
               time.sleep(0.1)
               pro.release('B')
               time.sleep(0.1)
               pro.press('B')
               time.sleep(0.1)
               pro.release('B')
               time.sleep(0.1)
               pro.press('B')
               time.sleep(0.1)
               pro.release('B')
            if progress in YY_1:
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.8)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
            if progress in YY_2:
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
               time.sleep(0.1)
               pro.press('Y')
               time.sleep(0.1)
               pro.release('Y')
            if progress not in REPEAT_1:
               completed.append(progress)

    # 强制复位比赛详情页
        pro.press_group(['B'] * 2, 0.2)
        time.sleep(1)
        for index in range(15):
            time.sleep(0.2)
            has_next = OCR.has_next()
            logger.info(f"has_next = {has_next}")
            if has_next:
                pro.press_group(['B'] * 1, 0.2)
                break
        for index in range(20):
            has_next = OCR.has_next()
            logger.info(f"has_next = {has_next}")
            if has_next:
                pro.press_group(['B'] * 1, 0.2)
            else:
                break
        time.sleep(8)
        pro.press_button('B', 0) # no reward, so no need of so many  B
        time.sleep(3)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if page.name == "star_up":
           pro.press_button('B', 0)

# 复位到生涯0 第四章 Euro Show Down 12永恒之城（固定代码勿动）
while career_select == 0 and career_time != 0:
    for index in range(4):
        pro.press_group(['B'] * 5, 1)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
            logger.info(f"main menu")
            break
    time.sleep(2)
    pro.press_group(['DPAD_DOWN'] * 5, 0.1)
    pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
    pro.press_group(['A'], 2)
    pro.press_group(['B'] * 2, 1)
    pro.press_group(['A'], 2)
    pro.press_group(['ZR'] * 3, 1)
    pro.press_group(['DPAD_RIGHT'] * 3, 0.5)
    pro.press_button('A', 0)
    for index in range(20):
        time.sleep(0.5)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if "THE" in page.text or "ETERNAL" in page.text or "CITY" in page.text:
            break
    if free_pack == 1 and ("FREE" in page.text or "Free" in page.text):
        for index in range(4):
            pro.press_group(['B'] * 5, 1)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")
            if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                logger.info(f"main menu")
                break
        time.sleep(2)
        pro.press_group(['DPAD_DOWN'] * 5, 0.1)
        pro.press_group(['DPAD_LEFT'] * 8, 0.1)
        pro.press_group(['A'], 0.5)
        pro.press_group(['DPAD_UP'], 0.5)
        pro.press_group(['A'] * 2, 5)
        page = OCR.get_page()
        if page.has_text("CLASSIC PACK.*POSSIBLE CONTENT"):
            pro.press_group(['A'] * 3, 3)
            pro.press_group(['B'], 0.5)
        else:
            logger.info(f"Failed to access free pack, current page = {page.name}")
    elif "THE" in page.text or "ETERNAL" in page.text or "CITY" in page.text:
        break
        
# 生涯0 第四章 Euro Show Down 12永恒之城寻路文件
LL = [4,5]
L = [0,1,29,30,31,32,38,39,40,43,44,60,61,62,82,83,84]
RR = []
R = [51,52,53,74]
B = ["19-4.5","20-4","36-0.1","53-2","54-1.5","63-0.1","69-0.1","88-1.5","89-1"]
BB = []
YY_1 = [9,10,11,12,13,36,64,65,96,97]#蓝喷
YY_2 = [29,30,33,34,46,47,58,59,71,72,80,81,91,92,93]#紫喷
REPEAT_1 = [0]#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机

# （固定代码勿动）
B = {int(item.split('-')[0]): float(item.split('-')[1]) for item in B}

car_select = 0
car_select_times = 0
car_select_need = True

career0_col = [item[1] for item in career0_car]
max_career0_col = max(career0_col) + 5

if hunt_take_up_time == 1:
    career_start_time = specialhunt_start_time
else:
    career_start_time = time.time()
race_times = 0
while career_select == 0 and career_time != 0:
    elapsed_time = time.time() - career_start_time
    logger.info(f"career0_elapsed/total_time = {elapsed_time:.0f} / {career_time * 60} seconds")
    if elapsed_time >= career_time * 60:
        break   
    logger.info(f"race_times = {race_times + 1}")
    race_times += 1

# 从生涯0 第四章 Euro Show Down 详情页进入至车辆详情
    while True:
        pro.press_group(['DPAD_UP'] * 6, 0.1)
        time.sleep(0.1)
        pro.press_group(['DPAD_DOWN'] * 1, 0.1)
        time.sleep(0.5)
        pro.press_button('A', 0)
        for index in range(20):
            time.sleep(0.5)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")
            if "CITY" in page.text:
               break
        if free_pack == 1 and ("FREE" in page.text or "Free" in page.text):
           race_times -= 1
           for index in range(4):
               pro.press_group(['B'] * 5, 1)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                   logger.info(f"main menu")
                   break
           time.sleep(2)
           pro.press_group(['DPAD_DOWN'] * 5, 0.1)
           pro.press_group(['DPAD_LEFT'] * 8, 0.1)
           pro.press_group(['A'], 0.5)
           pro.press_group(['DPAD_UP'], 0.5)
           pro.press_group(['A'] * 2, 5)
           page = OCR.get_page()
           if page.has_text("CLASSIC PACK.*POSSIBLE CONTENT"):
               pro.press_group(['A'] * 3, 3)
               pro.press_group(['B'], 0.5)
           else:
               logger.info(f"Failed to access free pack, current page = {page.name}")
           for index in range(4):
               pro.press_group(['B'] * 5, 1)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                  logger.info(f"main menu")
                  break
           time.sleep(2)
           pro.press_group(['DPAD_DOWN'] * 5, 0.1)
           pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
           pro.press_group(['A'], 2)
           pro.press_group(['B'] * 2, 1)
           pro.press_group(['A'], 2)
           pro.press_group(['ZR'] * 3, 1)
           pro.press_group(['DPAD_RIGHT'] * 3, 0.5)
           pro.press_button('A', 0)
           for index in range(20):
               time.sleep(0.5)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if "THE" in page.text or "ETERNAL" in page.text or "CITY" in page.text:
                  break
           continue
        if "CITY" in page.text:
           pro.press_group(['A'] * 4, 0.5)
           for index in range(20):
               time.sleep(0.5)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if page.name == "select_car":
                  break
        else:
           for index in range(4):
               pro.press_group(['B'] * 5, 1)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                  logger.info(f"main menu")
                  break
           time.sleep(2)
           pro.press_group(['DPAD_DOWN'] * 5, 0.1)
           pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
           pro.press_group(['A'], 2)
           pro.press_group(['B'] * 2, 1)
           pro.press_group(['A'], 2)
           pro.press_group(['ZR'] * 3, 1)
           pro.press_group(['DPAD_RIGHT'] * 3, 0.5)
           pro.press_button('A', 0)
           for index in range(20):
               time.sleep(0.5)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if "THE" in page.text or "ETERNAL" in page.text or "CITY" in page.text:
                  break
           continue
        if page.name == "select_car":
           break
        else:
           for index in range(4):
               pro.press_group(['B'] * 5, 1)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                  logger.info(f"main menu")
                  break
           time.sleep(2)
           pro.press_group(['DPAD_DOWN'] * 5, 0.1)
           pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
           pro.press_group(['A'], 2)
           pro.press_group(['B'] * 2, 1)
           pro.press_group(['A'], 2)
           pro.press_group(['ZR'] * 3, 1)
           pro.press_group(['DPAD_RIGHT'] * 3, 0.5)
           pro.press_button('A', 0)
           for index in range(20):
               time.sleep(0.5)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if "THE" in page.text or "ETERNAL" in page.text or "CITY" in page.text:
                  break
           continue
    while True:
       if car_select_need:
          # 第一次复位到左上
          if car_select == 0:
             time.sleep(0.2)
             pro.press_group(['DPAD_LEFT'] * max_career0_col, 0)
             time.sleep(0.2)
             pro.press_group(['DPAD_DOWN', 'DPAD_DOWN', 'DPAD_UP'], 0.2)
             if career0_car[0][0] == 2:
                pro.press_group(['DPAD_DOWN'] * 2, 0.1)
             pro.press_group(['DPAD_RIGHT'] * (career0_car[0][1] - 1), 0.2)
          # 行
          else: 
              if career0_car[car_select][0] == 1 and career0_car[car_select - 1][0] == 2:
                 time.sleep(0.2)
                 pro.press_group(['DPAD_UP'] * 1, 0.2)
              if career0_car[car_select][0] == 2 and career0_car[car_select - 1][0] == 1:
                 time.sleep(0.2)
                 pro.press_group(['DPAD_DOWN'] * 2, 0.1)
          # 列
              if career0_car[car_select][1] > career0_car[car_select - 1][1]:
                 time.sleep(0.2)
                 pro.press_group(['DPAD_RIGHT'] * (career0_car[car_select][1] - career0_car[car_select - 1][1]), 0.2)
              if career0_car[car_select][1] < career0_car[car_select - 1][1]:
                 time.sleep(0.2)
                 pro.press_group(['DPAD_LEFT'] * (career0_car[car_select - 1][1] - career0_car[car_select][1]), 0.2)
       time.sleep(0.2)
       pro.press_button('A', 0)
       for index in range(20):
           time.sleep(0.5)
           page = OCR.get_page()
           logger.info(f"page name = {page.name}")
           if page.name == "car_info":
              break
       if page.name == "select_car":
          pro.press_button('A', 0)
          time.sleep(3)
          page = OCR.get_page()
          logger.info(f"page name = {page.name}")
       mode = consts.car_hunt_zh
       states_a = OCR.has_play(mode)
       logger.info(f"states_a = {states_a}")
       mode = consts.legendary_hunt_zh
       states_b = OCR.has_play(mode)
       logger.info(f"states_b = {states_b}")
       mode = consts.custom_event_zh
       states_c = OCR.has_play(mode)
       logger.info(f"states_c = {states_c}")
       if not states_a and not states_b and not states_c and page.name == "car_info" and REFILL_GAS == 1:
          time.sleep(0.5)
          pro.press_group(['DPAD_RIGHT'] * 5, 0.1)
          time.sleep(1)
          pro.press_group(['A'] * 2, 2)
          car_select_need = False
          car_select_times = 0
          break
       elif not states_a and not states_b and not states_c and page.name == "car_info" and REFILL_GAS == 0:
          time.sleep(0.5)
          pro.press_button("B", 0)
          for index in range(20):
              time.sleep(0.5)
              page = OCR.get_page()
              logger.info(f"page name = {page.name}")
              if page.name == "select_car":
                 break
          if page.name != "select_car":
             pro.press_button('B', 0)
          car_select_need = True
          if car_select < len(career0_car) - 1:
             car_select = car_select + 1
          else:
             car_select = 0
          car_select_times = car_select_times + 1
       elif states_a or states_b or states_c:
          car_select_need = False
          car_select_times = 0
          break

# 检测play按钮是否有效（固定代码勿动）
    if states_a or states_b or states_c or page.name == "searching" or page.name == "loading_race" or page.name == "racing":
       pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','A'], 0.1)
       time.sleep(3)
       page = OCR.get_page()
       logger.info(f"page name = {page.name}")
       if page.name == "car_info":
          time.sleep(2)
          page = OCR.get_page()
          logger.info(f"page name = {page.name}")
          mode = consts.car_hunt_zh
          states_a = OCR.has_play(mode)
          logger.info(f"states_a = {states_a}")
          mode = consts.legendary_hunt_zh
          states_b = OCR.has_play(mode)
          logger.info(f"states_b = {states_b}")
          mode = consts.custom_event_zh
          states_c = OCR.has_play(mode)
          logger.info(f"states_c = {states_c}")
          if states_a or states_b or states_c:
             pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','A'], 0.1)
             time.sleep(3)
             page = OCR.get_page()
             logger.info(f"page name = {page.name}")
             if page.name == "car_info" or page.name == "switch_home":
                break
          else:
             break
    else:
        break

# 检测页面蓝币页面（固定代码勿动）
    if page.name == "tickets" or "REFILL" in page.text:
       break

# 寻路文件按进度执行（固定代码勿动）
    completed = []
    index_a = 0
    index_b = 0
    index_c = 0
    for index in range(1000):
        progress = OCR.get_time_progress()
        logger.info(f"progress = {progress}")
        if progress == -1:
           index_c = index_b + 1
           index_b = index_a + 1
           index_a = index
           if index_a == index_b and index_b == index_c:
              has_next = OCR.has_next()
              logger.info(f"has_next = {has_next}")
              if has_next:
                 break
        if progress in completed:
           continue

# 特殊进度优先部分开始（以下可修改,若无需特殊进度，可删除）

# 特殊进度优先部分结束（固定代码勿动）
        if progress in LL:
           pro.press_group(['DPAD_LEFT'] * 2, 0.1)
        if progress in L:
           pro.press_button("DPAD_LEFT", 0)
        if progress in RR:
           pro.press_group(['DPAD_RIGHT'] * 2, 0.1)
        if progress in R:
           pro.press_button("DPAD_RIGHT", 0)
        if progress in B:
           duration = B.get(progress)
           pro.press_buttons("B", down=duration)
        if progress in BB:
           pro.press('B')
           time.sleep(0.1)
           pro.release('B')
           time.sleep(0.1)
           pro.press('B')
           time.sleep(0.1)
           pro.release('B')
           time.sleep(0.1)
           pro.press('B')
           time.sleep(0.1)
           pro.release('B')
        if progress in YY_1:
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.8)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
        if progress in YY_2:
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
        if progress not in REPEAT_1:
           completed.append(progress)

# 正常领包复位比赛详情页
    pro.press_group(['B'] * 2, 0.2)
    time.sleep(1)
    for index in range(15):
        time.sleep(0.2)
        has_next = OCR.has_next()
        logger.info(f"has_next = {has_next}")
        if has_next:
            pro.press_group(['B'] * 1, 0.2)
            break
    for index in range(20):
        has_next = OCR.has_next()
        logger.info(f"has_next = {has_next}")
        if has_next:
            pro.press_group(['B'] * 1, 0.2)
        else:
            break
    for index in range(20):
        time.sleep(0.5)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if "THE" in page.text or "ETERNAL" in page.text or "CITY" in page.text:
           break
    if "THE" not in page.text and "ETERNAL" not in page.text and "CITY" not in page.text:
       pro.press_button('B', 0)
       time.sleep(8)

# 复位到生涯1 第六章 British Tour 4紫色大道（固定代码勿动）
while career_select == 1 and career_time != 0:
    for index in range(4):
        pro.press_group(['B'] * 5, 1)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
            logger.info(f"main menu")
            break
    time.sleep(2)
    pro.press_group(['DPAD_DOWN'] * 5, 0.1)
    pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
    pro.press_group(['A'], 2)
    pro.press_group(['B'] * 2, 1)
    pro.press_group(['A'], 2)
    pro.press_group(['ZR'] * 5, 1)
    pro.press_group(['DPAD_RIGHT'] * 1, 0.5)
    pro.press_button('A', 0)
    for index in range(20):
        time.sleep(0.5)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if "BALL" in page.text or "POL" in page.text:
            break
    if free_pack == 1 and ("FREE" in page.text or "Free" in page.text):
        for index in range(4):
            pro.press_group(['B'] * 5, 1)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")
            if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                logger.info(f"main menu")
                break
        time.sleep(2)
        pro.press_group(['DPAD_DOWN'] * 5, 0.1)
        pro.press_group(['DPAD_LEFT'] * 8, 0.1)
        pro.press_group(['A'], 0.5)
        pro.press_group(['DPAD_UP'], 0.5)
        pro.press_group(['A'] * 2, 5)
        page = OCR.get_page()
        if page.has_text("CLASSIC PACK.*POSSIBLE CONTENT"):
            pro.press_group(['A'] * 3, 3)
            pro.press_group(['B'], 0.5)
        else:
            logger.info(f"Failed to access free pack, current page = {page.name}")
    elif "BALL" in page.text or "POL" in page.text:
        break
        
# 生涯1 第六章 British Tour 4紫色大道寻路文件
LL = []
L = [15,16,17,18,26,27,28,35,36,80,81,82]
RR = []
R = [0,1]
B = ["28-0.1","36-0.1","41-0.1","55-0.1","65-2","66-1.5","81-0.1"]
BB = [74]#89,90
YY_1 = [32,33,49,50,57,58,81,82,83]#蓝喷
YY_2 = [12,13,14,24,25,36,37,38,65,66,70,71,75,76,77,78,86,87,91,92,93,94]#紫喷
REPEAT_1 = [0,1]#需要重复执行操作的进度，比如图比较长，同一个进度需要多次操作才能对应上选路时机

# （固定代码勿动）
B = {int(item.split('-')[0]): float(item.split('-')[1]) for item in B}

car_select = 0
car_select_times = 0
car_select_need = True

career1_col = [item[1] for item in career1_car]
max_career1_col = max(career1_col) + 5

if hunt_take_up_time == 1:
    career_start_time = specialhunt_start_time
else:
    career_start_time = time.time()
race_times = 0
while career_select == 1 and career_time != 0:
    elapsed_time = time.time() - career_start_time
    logger.info(f"career1_elapsed/total_time = {elapsed_time:.0f} / {career_time * 60} seconds")
    if elapsed_time >= career_time * 60:
        break   
    logger.info(f"race_times = {race_times + 1}")
    race_times += 1

# 从生涯1 第六章 British Tour 详情页进入至车辆详情
    while True:
        pro.press_group(['DPAD_UP'] * 2, 0.1)
        time.sleep(0.1)
        pro.press_group(['DPAD_LEFT'] * 1, 0.1)
        time.sleep(0.5)
        pro.press_button('A', 0)
        for index in range(20):
            time.sleep(0.5)
            page = OCR.get_page()
            logger.info(f"page name = {page.name}")
            if "PUR" in page.text or "PLE" in page.text or "BOUL" in page.text or "VARD" in page.text:
               break
        if free_pack == 1 and ("FREE" in page.text or "Free" in page.text):
           race_times -= 1
           for index in range(4):
               pro.press_group(['B'] * 5, 1)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                   logger.info(f"main menu")
                   break
           time.sleep(2)
           pro.press_group(['DPAD_DOWN'] * 5, 0.1)
           pro.press_group(['DPAD_LEFT'] * 8, 0.1)
           pro.press_group(['A'], 0.5)
           pro.press_group(['DPAD_UP'], 0.5)
           pro.press_group(['A'] * 2, 5)
           page = OCR.get_page()
           if page.has_text("CLASSIC PACK.*POSSIBLE CONTENT"):
               pro.press_group(['A'] * 3, 3)
               pro.press_group(['B'], 0.5)
           else:
               logger.info(f"Failed to access free pack, current page = {page.name}")
           for index in range(4):
               pro.press_group(['B'] * 5, 1)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                  logger.info(f"main menu")
                  break
           time.sleep(2)
           pro.press_group(['DPAD_DOWN'] * 5, 0.1)
           pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
           pro.press_group(['A'], 2)
           pro.press_group(['B'] * 2, 1)
           pro.press_group(['A'], 2)
           pro.press_group(['ZR'] * 5, 1)
           pro.press_group(['DPAD_RIGHT'] * 1, 0.5)
           pro.press_button('A', 0)
           for index in range(20):
               time.sleep(0.5)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if "BALL" in page.text or "POL" in page.text:
                  break
           continue
        if "PUR" in page.text or "PLE" in page.text or "BOUL" in page.text or "VARD" in page.text:
           pro.press_group(['A'] * 2, 0.5)
           for index in range(20):
               time.sleep(0.5)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if page.name == "select_car":
                  break
        else:
           for index in range(4):
               pro.press_group(['B'] * 5, 1)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                  logger.info(f"main menu")
                  break
           time.sleep(2)
           pro.press_group(['DPAD_DOWN'] * 5, 0.1)
           pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
           pro.press_group(['A'], 2)
           pro.press_group(['B'] * 2, 1)
           pro.press_group(['A'], 2)
           pro.press_group(['ZR'] * 5, 1)
           pro.press_group(['DPAD_RIGHT'] * 1, 0.5)
           pro.press_button('A', 0)
           for index in range(20):
               time.sleep(0.5)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if "BALL" in page.text or "POL" in page.text:
                  break
           continue
        if page.name == "select_car":
           break
        else:
           for index in range(4):
               pro.press_group(['B'] * 5, 1)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
                  logger.info(f"main menu")
                  break
           time.sleep(2)
           pro.press_group(['DPAD_DOWN'] * 5, 0.1)
           pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
           pro.press_group(['A'], 2)
           pro.press_group(['B'] * 2, 1)
           pro.press_group(['A'], 2)
           pro.press_group(['ZR'] * 5, 1)
           pro.press_group(['DPAD_RIGHT'] * 1, 0.5)
           pro.press_button('A', 0)
           for index in range(20):
               time.sleep(0.5)
               page = OCR.get_page()
               logger.info(f"page name = {page.name}")
               if "BALL" in page.text or "POL" in page.text:
                  break
           continue
    while True:
       if car_select_need:
          # 第一次复位到左上
          if car_select == 0:
             time.sleep(0.2)
             pro.press_group(['DPAD_LEFT'] * max_career1_col, 0)
             time.sleep(0.2)
             pro.press_group(['DPAD_DOWN', 'DPAD_DOWN', 'DPAD_UP'], 0.2)
             if career1_car[0][0] == 2:
                pro.press_group(['DPAD_DOWN'] * 2, 0.1)
             pro.press_group(['DPAD_RIGHT'] * (career1_car[0][1] - 1), 0.2)
          # 行
          else: 
              if career1_car[car_select][0] == 1 and career1_car[car_select - 1][0] == 2:
                 time.sleep(0.2)
                 pro.press_group(['DPAD_UP'] * 1, 0.2)
              if career1_car[car_select][0] == 2 and career1_car[car_select - 1][0] == 1:
                 time.sleep(0.2)
                 pro.press_group(['DPAD_DOWN'] * 2, 0.1)
          # 列
              if career1_car[car_select][1] > career1_car[car_select - 1][1]:
                 time.sleep(0.2)
                 pro.press_group(['DPAD_RIGHT'] * (career1_car[car_select][1] - career1_car[car_select - 1][1]), 0.2)
              if career1_car[car_select][1] < career1_car[car_select - 1][1]:
                 time.sleep(0.2)
                 pro.press_group(['DPAD_LEFT'] * (career1_car[car_select - 1][1] - career1_car[car_select][1]), 0.2)
       time.sleep(0.2)
       pro.press_button('A', 0)
       for index in range(20):
           time.sleep(0.5)
           page = OCR.get_page()
           logger.info(f"page name = {page.name}")
           if page.name == "car_info":
              break
       if page.name == "select_car":
          pro.press_button('A', 0)
          time.sleep(3)
          page = OCR.get_page()
          logger.info(f"page name = {page.name}")
       mode = consts.car_hunt_zh
       states_a = OCR.has_play(mode)
       logger.info(f"states_a = {states_a}")
       mode = consts.legendary_hunt_zh
       states_b = OCR.has_play(mode)
       logger.info(f"states_b = {states_b}")
       mode = consts.custom_event_zh
       states_c = OCR.has_play(mode)
       logger.info(f"states_c = {states_c}")
       if not states_a and not states_b and not states_c and page.name == "car_info" and REFILL_GAS == 1:
          time.sleep(0.5)
          pro.press_group(['DPAD_RIGHT'] * 5, 0.1)
          time.sleep(1)
          pro.press_group(['A'] * 2, 2)
          car_select_need = False
          car_select_times = 0
          break
       elif not states_a and not states_b and not states_c and page.name == "car_info" and REFILL_GAS == 0:
          time.sleep(0.5)
          pro.press_button("B", 0)
          for index in range(20):
              time.sleep(0.5)
              page = OCR.get_page()
              logger.info(f"page name = {page.name}")
              if page.name == "select_car":
                 break
          if page.name != "select_car":
             pro.press_button('B', 0)
          car_select_need = True
          if car_select < len(career1_car) - 1:
             car_select = car_select + 1
          else:
             car_select = 0
          car_select_times = car_select_times + 1
       elif states_a or states_b or states_c:
          car_select_need = False
          car_select_times = 0
          break

# 检测play按钮是否有效（固定代码勿动）
    if states_a or states_b or states_c or page.name == "searching" or page.name == "loading_race" or page.name == "racing":
       pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','A'], 0.1)
       time.sleep(3)
       page = OCR.get_page()
       logger.info(f"page name = {page.name}")
       if page.name == "car_info":
          time.sleep(2)
          page = OCR.get_page()
          logger.info(f"page name = {page.name}")
          mode = consts.car_hunt_zh
          states_a = OCR.has_play(mode)
          logger.info(f"states_a = {states_a}")
          mode = consts.legendary_hunt_zh
          states_b = OCR.has_play(mode)
          logger.info(f"states_b = {states_b}")
          mode = consts.custom_event_zh
          states_c = OCR.has_play(mode)
          logger.info(f"states_c = {states_c}")
          if states_a or states_b or states_c:
             pro.press_group(['DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','DPAD_RIGHT','A'], 0.1)
             time.sleep(3)
             page = OCR.get_page()
             logger.info(f"page name = {page.name}")
             if page.name == "car_info" or page.name == "switch_home":
                break
          else:
             break
    else:
        break

# 检测页面蓝币页面（固定代码勿动）
    if page.name == "tickets" or "REFILL" in page.text:
       break

# 寻路文件按进度执行（固定代码勿动）
    completed = []
    index_a = 0
    index_b = 0
    index_c = 0
    for index in range(1000):
        progress = OCR.get_new_progress()
        logger.info(f"progress = {progress}")
        if progress == -1:
           index_c = index_b + 1
           index_b = index_a + 1
           index_a = index
           if index_a == index_b and index_b == index_c:
              has_next = OCR.has_next()
              logger.info(f"has_next = {has_next}")
              if has_next:
                 break
        if progress in completed:
           continue

# 特殊进度优先部分开始（以下可修改,若无需特殊进度，可删除）
        if progress == 2 or progress == 3:
           if progress - index_a > 1: 
              index_a = progress
              continue
        if progress >= 0:
           index_a = progress
        if progress == 2:
           pro.press_button("DPAD_RIGHT", 0)
           pro.press('B')
           time.sleep(4.8)
           #pro.press('DPAD_LEFT')
           time.sleep(0.1)
           pro.release('DPAD_LEFT')
           pro.press('B')
           time.sleep(0.5)
           pro.release('B')
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           completed.append(3)
        if progress == 3:
           pro.press('B')
           time.sleep(4.3)
           #pro.press('DPAD_LEFT')
           time.sleep(0.1)
           pro.release('DPAD_LEFT')
           pro.press('B')
           time.sleep(0.5)
           pro.release('B')
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
        if progress == 21:
           pro.press('B')
           time.sleep(1)
           pro.press('DPAD_LEFT')
           time.sleep(0.1)
           pro.release('DPAD_LEFT')
           pro.press('B')
           time.sleep(1.1)
           pro.release('B')
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           completed.append(23)
        if progress == 23:
           pro.press_button("DPAD_LEFT", 0)
           pro.press('B')
           time.sleep(1.1)
           pro.release('B')
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')

# 特殊进度优先部分结束（固定代码勿动）
        if progress in LL:
           pro.press_group(['DPAD_LEFT'] * 2, 0.1)
        if progress in L:
           pro.press_button("DPAD_LEFT", 0)
        if progress in RR:
           pro.press_group(['DPAD_RIGHT'] * 2, 0.1)
        if progress in R:
           pro.press_button("DPAD_RIGHT", 0)
        if progress in B:
           duration = B.get(progress)
           pro.press_buttons("B", down=duration)
        if progress in BB:
           pro.press('B')
           time.sleep(0.1)
           pro.release('B')
           time.sleep(0.1)
           pro.press('B')
           time.sleep(0.1)
           pro.release('B')
           time.sleep(0.1)
           pro.press('B')
           time.sleep(0.1)
           pro.release('B')
        if progress in YY_1:
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.8)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
        if progress in YY_2:
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
           time.sleep(0.1)
           pro.press('Y')
           time.sleep(0.1)
           pro.release('Y')
        if progress not in REPEAT_1:
           completed.append(progress)

# 正常领包复位比赛详情页
    pro.press_group(['B'] * 2, 0.2)
    time.sleep(1)
    for index in range(15):
        time.sleep(0.2)
        has_next = OCR.has_next()
        logger.info(f"has_next = {has_next}")
        if has_next:
            pro.press_group(['B'] * 1, 0.2)
            break
    for index in range(20):
        has_next = OCR.has_next()
        logger.info(f"has_next = {has_next}")
        if has_next:
            pro.press_group(['B'] * 1, 0.2)
        else:
            break
    for index in range(20):
        time.sleep(0.5)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if "BALL" in page.text or "POL" in page.text:
           break
    if "BALL" not in page.text and "POL" not in page.text:
       pro.press_button('B', 0)
       time.sleep(8)
       
# 自定义循环结束复位到目标页面（固定代码勿动）
if target_page != 0:
    for index in range(4):
        pro.press_group(['B'] * 5, 1)
        page = OCR.get_page()
        logger.info(f"page name = {page.name}")
        if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
            logger.info(f"main menu")
            break
    time.sleep(2)
    pro.press_group(['DPAD_DOWN'] * 5, 0.1)
    pro.press_group(['DPAD_RIGHT'] * 7, 0.1)
    pro.press_group(['A'], 2)
    pro.press_group(['B'] * 2, 1)
    pro.press_group(['ZL'] * 4, 1)
    page = OCR.get_page()
    logger.info(f"page name = {page.name}")
    if page.name == "multi_player" and target_page == 1:
        pro.press_group(['ZL'], 1)
    elif page.name == "multi_player" and target_page == 2:
        time.sleep(0.5)
    elif page.name == "multi_player" and target_page == 3:
        pro.press_group(['A'], 1)
    elif page.name == "multi_player" and target_page == 4:
        pro.press_group(['DPAD_DOWN', 'A'], 1)
    elif page.name != "daily_events" and page.name != "multi_player":
        pro.press_group(['ZL'], 1)
    
# auto辅助运行控制（固定代码）
if auto_time != 0:
    G.input_queue.put("run")

# BBYY运行控制（固定代码）
if hunt_take_up_time == 1 and career_time == 0:
    auto_start_time = specialhunt_start_time
else:
    auto_start_time = time.time()
Operation_pos = 0
while enable_BBYY == 0 and auto_time != 0:
    time.sleep(20)
    elapsed_time = time.time() - auto_start_time
    logger.info(f"disabled_BBYY_elapsed/total_time = {elapsed_time:.0f} / {auto_time * 60} seconds")
    if elapsed_time >= auto_time * 60:
        break   
while enable_BBYY == 1 and auto_time != 0:
    elapsed_time = time.time() - auto_start_time
    logger.info(f"enabled_BBYY_elapsed/total_time = {elapsed_time:.0f} / {auto_time * 60} seconds")
    if elapsed_time >= auto_time * 60:
        break
    progress = OCR.get_new_progress()
    if progress == -1:
        Operation_pos = 0
    if progress < Operation_progress - 10:
        time.sleep((Operation_progress - 10 - progress)*0.3)
    elif progress >= Operation_progress - 10 and progress < Operation_progress:
        get_pos = OCR.get_pos()
        if get_pos:
            Operation_pos = get_pos
        time.sleep(0.5)
    elif progress >= Operation_progress and progress < 98:
        if Operation_pos >= BBYY_pos:
            for index in range(50):
                if progress >= Operation_progress and progress < 98:
                    pro.press('B')
                    time.sleep(0.1)
                    pro.release('B')
                    time.sleep(0.1)
                    pro.press('B')
                    time.sleep(0.1)
                    pro.release('B')
                    progress = OCR.get_progress()
                else:
                    break
            logger.info(f"BB_OVER, Operation_pos = {Operation_pos}")
            time.sleep(10)
        elif Operation_pos >= 1:
            pro.press('B')
            time.sleep(0.1)
            pro.release('B')
            time.sleep(0.1)
            pro.press('Y')
            time.sleep(0.1)
            pro.release('Y')
            time.sleep(0.1)
            pro.press('Y')
            time.sleep(0.1)
            pro.release('Y')
            time.sleep(0.1)
            pro.press('Y')
            time.sleep(0.1)
            pro.release('Y')
            for index in range(50):
                 progress = OCR.get_progress()
                 if progress >= Operation_progress and progress < 98:
                     pro.press('Y')
                     time.sleep(0.1)
                     pro.release('Y')
                     time.sleep(0.1)
                     pro.press('Y')
                     time.sleep(0.1)
                     pro.release('Y')
                 else:
                     break
            logger.info(f"YY_OVER, Operation_pos = {Operation_pos}")
            time.sleep(10)
        elif Operation_pos == 0:
            logger.info(f"Failed to obtain pos")
            time.sleep(10)
    else:
        logger.info(f"finish competition, Operation_pos = {Operation_pos}")
        time.sleep(10)

# auto辅助停止控制（固定代码）
while auto_time != 0 and auto_stop == 0:
    time.sleep(1)
    progress = OCR.get_new_progress()
    logger.info(f"progress = {progress}")
    if progress >= 70 and progress <80:
       for queue_stop in range(20):
           G.input_queue.put("stop")
           time.sleep(0.5)
       break
while auto_time != 0 and (auto_stop == 0 or auto_stop == 1):
    time.sleep(1)
    has_next = OCR.has_next()
    logger.info(f"has_next = {has_next}")
    if has_next:
       for queue_stop in range(20):
           G.input_queue.put("stop")
           time.sleep(0.5)
       break
auto_start_time = time.time()
while auto_time != 0 and auto_stop == 2:
    time.sleep(0.5)
    G.input_queue.put("stop")
    elapsed_time = time.time() - auto_start_time
    logger.info(f"auto_stop_elapsed/total_time = {elapsed_time:.0f} / 180 seconds")
    if elapsed_time >= 180:
        break

# 重启控制（固定代码）
while enable_restart == 1:
    """重启游戏"""
    # 回到主页
    pro.press_button('HOME', 3)
    # 关闭
    pro.press_group(['X'] * 2, 1)
    # 按一下确认关闭，再打开
    pro.press_group(['A'] * 3, 2)
    for index in range(30):
        pro.press_group(['A'] * 4, 1)
        page = OCR.get_page()
        logger.info(f"page text = {page.text}")
        if ("ASP" in page.text or "NIN" in page.text or "NDO" in page.text) and page.name != "switch_home":
            pro.press_group(['A'] * 4, 1)
            logger.info(f"enter")
            break
    for index in range(120):
        time.sleep(1)
        page = OCR.get_page()
        logger.info(f"page text = {page.text}")
        if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
            logger.info(f"main menu")
            break
    if ("EVENTS" in page.text or "PLAYER" in page.text) and ("SCREEN" in page.text or "CAREER" in page.text):
        logger.info(f"Restart completed")
        break