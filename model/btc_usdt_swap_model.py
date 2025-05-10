import os

from peewee import SqliteDatabase

from base_model import BaseDataModel, BaseTrendDataModel

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 定义正常数据库
btc_db = SqliteDatabase(os.path.join(current_dir, "database/btc_usdt_swap.db"))
# 定义详细的数据库
detail_btc_db = SqliteDatabase(
    os.path.join(current_dir, "database/btc_usdt_swap_detail.db")
)


# 定义BTC一周数据模型
class BTCUSDTWeekDataModel(BaseTrendDataModel):
    class Meta:
        database = btc_db


# 定义BTC一日数据模型
class BTCUSDTDayDataModel(BaseTrendDataModel):
    class Meta:
        database = btc_db


# 定义BTC12小时数据模型
class BTCUSDT12HDataModel(BaseTrendDataModel):
    class Meta:
        database = btc_db


# 定义BTC6小时数据模型
class BTCUSDT6HDataModel(BaseTrendDataModel):
    class Meta:
        database = btc_db


# 定义BTC4小时数据模型
class BTCUSDT4HDataModel(BaseTrendDataModel):
    class Meta:
        database = btc_db


# 定义BTC2小时数据模型
class BTCUSDT2HDataModel(BaseTrendDataModel):
    class Meta:
        database = btc_db


# 定义BTC1小时数据模型
class BTCUSDT1HDataModel(BaseDataModel):
    class Meta:
        database = btc_db


# 定义BTC30分钟数据模型
class BTCUSDT30MinDataModel(BaseDataModel):
    class Meta:
        database = detail_btc_db


# 定义BTC15分钟数据模型
class BTCUSDT15MinDataModel(BaseDataModel):
    class Meta:
        database = detail_btc_db


# 定义BTC5分钟数据模型
class BTCUSDT5MinDataModel(BaseDataModel):
    class Meta:
        database = detail_btc_db


# 定义BTC3分钟数据模型
class BTCUSDT3MinDataModel(BaseDataModel):
    class Meta:
        database = detail_btc_db


# 定义BTC1分钟数据模型
class BTCUSDT1MinDataModel(BaseDataModel):
    class Meta:
        database = detail_btc_db


# 创建表
btc_db.connect()
btc_db.create_tables(
    [
        BTCUSDTWeekDataModel,
        BTCUSDTDayDataModel,
        BTCUSDT12HDataModel,
        BTCUSDT6HDataModel,
        BTCUSDT2HDataModel,
        BTCUSDT4HDataModel,
        BTCUSDT1HDataModel,
    ]
)

# 创建Detail表
detail_btc_db.connect()
detail_btc_db.create_tables(
    [
        BTCUSDT30MinDataModel,
        BTCUSDT15MinDataModel,
        BTCUSDT5MinDataModel,
        BTCUSDT3MinDataModel,
        BTCUSDT1MinDataModel,
    ]
)

# 启用性能优化
detail_btc_db.pragma("journal_mode", "wal")  # 启用 WAL 模式
detail_btc_db.pragma("synchronous", "off")  # 关闭同步模式（仅用于快速插入）
detail_btc_db.pragma("cache_size", -1024 * 64)  # 调整缓存大小（64MB）
