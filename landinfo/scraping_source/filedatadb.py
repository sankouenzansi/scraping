"""
DBへの挿入を行う
"""
import csv
import re
import traceback
from datetime import datetime

from dbconnection import DbConnect
from LandInfo import LandColumns1, LandColumns2, LandInfo1, LandInfo2

csvpath1 = ".\\venvtest\\Sourse\\scraping\\csv\\land_info_at1.csv"
csvpath2 = ".\\venvtest\\Sourse\\scraping\\csv\\land_info_at2.csv"

try:
    # DB操作のオブジェクトを生成　
    connect = DbConnect()

    # 各土地情報のオブジェクトを生成
    columns1 = LandColumns1()
    columns2 = LandColumns2()

    # csvファイルから情報を取り出して、DBに挿入

    # title,url,交通,所在地,物件種目,価格,坪単価,借地期間・地代（月額）,
    # 権利金,敷金 / 保証金,維持費等,その他一時金,設備,特記事項,備考,
    # 土地面積,坪数,最適用途,私道負担面積,土地権利,都市計画,用途地域,
    # 地勢,建ぺい率,容積率,接道状況,地目,国土法届出,セットバック,条件等,
    # 現況,引渡し（時期/方法）,物件番号,情報公開日,次回更新予定日 35
    with open(csvpath1, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            info_list = []
            for k, v in row.items():
                if k in columns1.column_list:
                    if (v == '－') or (v == '-'):
                        info_list.append(None)
                    else:
                        if (k == columns1.price) or \
                            (k == columns1.land_area) or \
                                (k == columns1.floor_space):
                            num = re.match("[0-9]+(.[0-9]+)",
                                           v.replace(",", ""))
                            if num:
                                info_list.append(float(num.group(0)))
                            else:
                                info_list.append(None)
                        elif (k == columns1.info_release_date) or \
                                (k == columns1.next_info_update_date):
                            info_list.append(
                                datetime.strptime(v, "%Y年%m月%d日"))
                        elif k == columns1.property_no:
                            info_list.append(int(v))
                        else:
                            info_list.append(v)
            land_info = LandInfo1(info_list)
            connect.db_insert1(land_info)

    # title,url,造成完成時期,引渡し時期,販売スケジュール,価格,最多価格帯,その他費用,
    # 土地面積,坪数,販売区画数,総区画数,お問い合わせ先,物件種目,所在地,交通,建蔽率/容積率,
    # 私道負担,接道情報,駐車場,設備,権利,用途地域,都市計画,地目,開発許可等番号,
    # 備考,売主,情報提供元,情報更新日,次回更新予定日,販売戸数/総戸数 32
    with open(csvpath2, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            info_list = []
            for k, v in row.items():
                if k in columns2.column_list:
                    if (v == '－') or (v == '-'):
                        info_list.append(None)
                    else:
                        if (k == columns2.price) or \
                            (k == columns2.land_area) or \
                                (k == columns2.floor_space):
                            num = re.match(
                                "[0-9]+(.[0-9]+)", v.replace(",", ""))
                            if num:
                                info_list.append(float(num.group(0)))
                            else:
                                info_list.append(None)
                        elif (k == columns2.info_update_date) or \
                                (k == columns2.next_info_update_date):
                            info_list.append(
                                datetime.strptime(v, "%Y年%m月%d日"))
                        else:
                            info_list.append(v)
            land_info = LandInfo2(info_list)
            connect.db_insert2(land_info)
    connect.db_commit()
except:
    # エラーが発生した場合、rollbackを行う
    print("-> error")
    print("---------------------------")
    print(traceback.format_exc())
    print("---------------------------")
    connect.db_rollback()
finally:
    # DBの接続を閉じる
    connect.db_close()

# DBへの挿入の完了を伝える旨
print("-> Insert data for db finish")
