import os

from peewee import SqliteDatabase

from base_model import BaseDataModel, BaseTrendDataModel

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 定义正常数据库
eth_db = SqliteDatabase(os.path.join(current_dir, "database/eth_usdt_swap.db"))
# 定义详细的数据库
detail_eth_db = SqliteDatabase(
    os.path.join(current_dir, "database/eth_usdt_swap_detail.db")
)


# 定义ETH一周数据模型
class ETHUSDTWeekDataModel(BaseTrendDataModel):
    class Meta:
        database = eth_db


# 定义ETH一日数据模型
class ETHUSDTDayDataModel(BaseTrendDataModel):
    class Meta:
        database = eth_db


# 定义ETH12小时数据模型
class ETHUSDT12HDataModel(BaseTrendDataModel):
    class Meta:
        database = eth_db


# 定义ETH6小时数据模型
class ETHUSDT6HDataModel(BaseTrendDataModel):
    class Meta:
        database = eth_db


# 定义ETH4小时数据模型
class ETHUSDT4HDataModel(BaseTrendDataModel):
    class Meta:
        database = eth_db


# 定义ETH2小时数据模型
class ETHUSDT2HDataModel(BaseTrendDataModel):
    class Meta:
        database = eth_db


# 定义ETH1小时数据模型
class ETHUSDT1HDataModel(BaseDataModel):
    class Meta:
        database = eth_db


# 定义ETH30分钟数据模型
class ETHUSDT30MinDataModel(BaseDataModel):
    class Meta:
        database = detail_eth_db


# 定义ETH15分钟数据模型
class ETHUSDT15MinDataModel(BaseDataModel):
    class Meta:
        database = detail_eth_db


# 定义ETH5分钟数据模型
class ETHUSDT5MinDataModel(BaseDataModel):
    class Meta:
        database = detail_eth_db


# 定义ETH3分钟数据模型
class ETHUSDT3MinDataModel(BaseDataModel):
    class Meta:
        database = detail_eth_db


# 定义ETH1分钟数据模型
class ETHUSDT1MinDataModel(BaseDataModel):
    class Meta:
        database = detail_eth_db


# 创建表
eth_db.connect()
eth_db.create_tables(
    [
        ETHUSDTWeekDataModel,
        ETHUSDTDayDataModel,
        ETHUSDT12HDataModel,
        ETHUSDT6HDataModel,
        ETHUSDT2HDataModel,
        ETHUSDT4HDataModel,
        ETHUSDT1HDataModel,
    ]
)

# 创建Detail表
detail_eth_db.connect()
detail_eth_db.create_tables(
    [
        ETHUSDT30MinDataModel,
        ETHUSDT15MinDataModel,
        ETHUSDT5MinDataModel,
        ETHUSDT3MinDataModel,
        ETHUSDT1MinDataModel,
    ]
)

# 启用性能优化
detail_eth_db.pragma("journal_mode", "wal")  # 启用 WAL 模式
detail_eth_db.pragma("synchronous", "off")  # 关闭同步模式（仅用于快速插入）
detail_eth_db.pragma("cache_size", -1024 * 64)  # 调整缓存大小（64MB）
