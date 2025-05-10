import datetime
import os
from peewee import Model, SqliteDatabase, CharField, BigIntegerField, DateTimeField

from model.btc_usdt_swap_model import (
    BTCUSDTWeekDataModel,
    BTCUSDTDayDataModel,
    BTCUSDT12HDataModel,
    BTCUSDT6HDataModel,
    BTCUSDT4HDataModel,
    BTCUSDT2HDataModel,
    BTCUSDT1HDataModel,
    BTCUSDT30MinDataModel,
    BTCUSDT15MinDataModel,
    BTCUSDT5MinDataModel,
    BTCUSDT3MinDataModel,
    BTCUSDT1MinDataModel,
)
from model.eth_usdt_swap_model import ETHUSDTWeekDataModel, ETHUSDTDayDataModel, ETHUSDT12HDataModel, \
    ETHUSDT6HDataModel, ETHUSDT4HDataModel, ETHUSDT2HDataModel, ETHUSDT1HDataModel, ETHUSDT30MinDataModel, \
    ETHUSDT15MinDataModel, ETHUSDT5MinDataModel, ETHUSDT3MinDataModel, ETHUSDT1MinDataModel

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 定义正常数据库
aggregate_db = SqliteDatabase(os.path.join(current_dir, "database/aggregate_data.db"))


class AggregateDataModel(Model):
    table_name = CharField(primary_key=True, unique=True)  # 记录表名
    record_timestamp = BigIntegerField(default=0)  # 记录的已经更新的时间
    record_time = DateTimeField(default=datetime.time)
    trend_timestamp = BigIntegerField(default=0)  # 趋势处理的时间
    trend_time = DateTimeField(default=datetime.time)

    class Meta:
        database = aggregate_db


# 创建表
aggregate_db.connect()
aggregate_db.create_tables([AggregateDataModel])
data_dict = [
    {"table_name": BTCUSDTWeekDataModel._meta.table_name},
    {"table_name": BTCUSDTDayDataModel._meta.table_name},
    {"table_name": BTCUSDT12HDataModel._meta.table_name},
    {"table_name": BTCUSDT6HDataModel._meta.table_name},
    {"table_name": BTCUSDT4HDataModel._meta.table_name},
    {"table_name": BTCUSDT2HDataModel._meta.table_name},
    {"table_name": BTCUSDT1HDataModel._meta.table_name},
    {"table_name": BTCUSDT30MinDataModel._meta.table_name},
    {"table_name": BTCUSDT15MinDataModel._meta.table_name},
    {"table_name": BTCUSDT5MinDataModel._meta.table_name},
    {"table_name": BTCUSDT3MinDataModel._meta.table_name},
    {"table_name": BTCUSDT1MinDataModel._meta.table_name},
    {"table_name": ETHUSDTWeekDataModel._meta.table_name},
    {"table_name": ETHUSDTDayDataModel._meta.table_name},
    {"table_name": ETHUSDT12HDataModel._meta.table_name},
    {"table_name": ETHUSDT6HDataModel._meta.table_name},
    {"table_name": ETHUSDT4HDataModel._meta.table_name},
    {"table_name": ETHUSDT2HDataModel._meta.table_name},
    {"table_name": ETHUSDT1HDataModel._meta.table_name},
    {"table_name": ETHUSDT30MinDataModel._meta.table_name},
    {"table_name": ETHUSDT15MinDataModel._meta.table_name},
    {"table_name": ETHUSDT5MinDataModel._meta.table_name},
    {"table_name": ETHUSDT3MinDataModel._meta.table_name},
    {"table_name": ETHUSDT1MinDataModel._meta.table_name},
]
with aggregate_db.atomic():
    AggregateDataModel.insert_many(data_dict).on_conflict_ignore().execute()
