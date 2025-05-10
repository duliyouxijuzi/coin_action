from eth_usdt_swap_model import *
from btc_usdt_swap_model import *
import time
from datetime import datetime
import okx.MarketData as MarketData

from model.model_manager_helper import AggregateDataModel, aggregate_db

marketDataAPI = MarketData.MarketAPI(flag="0")
# 这是输出开始时间,年 月 日 时
MASK_START_DATE = datetime(2025, 4, 30, 8)

def update_btc_all():
    update_btc_main()
    update_btc_detail()

def update_all():
    update_eth_all()
    update_btc_all()


def update_eth_all():
    update_eth_main()
    update_eth_detail()

def update_eth_month():
    fetch_and_store_data(
        ETHUSDTWeekDataModel, "ETH-USDT-SWAP", "1Wutc", 60 * 60 * 24 * 7
    )

def update_eth_main():
    fetch_and_store_data(
        ETHUSDTWeekDataModel, "ETH-USDT-SWAP", "1Wutc", 60 * 60 * 24 * 7
    )
    fetch_and_store_data(ETHUSDTDayDataModel, "ETH-USDT-SWAP", "1Dutc", 60 * 60 * 24)
    fetch_and_store_data(ETHUSDT12HDataModel, "ETH-USDT-SWAP", "12Hutc", 60 * 60 * 12)
    fetch_and_store_data(ETHUSDT6HDataModel, "ETH-USDT-SWAP", "6Hutc", 60 * 60 * 6)
    fetch_and_store_data(ETHUSDT4HDataModel, "ETH-USDT-SWAP", "4H", 60 * 60 * 4)
    fetch_and_store_data(ETHUSDT2HDataModel, "ETH-USDT-SWAP", "2H", 60 * 60 * 2)

def update_eth_detail():
    fetch_and_store_data(ETHUSDT1HDataModel, "ETH-USDT-SWAP", "1H", 60 * 60 * 1)
    fetch_and_store_data(ETHUSDT30MinDataModel, "ETH-USDT-SWAP", "30m", 60 * 30)
    fetch_and_store_data(ETHUSDT15MinDataModel, "ETH-USDT-SWAP", "15m", 60 * 15)
    fetch_and_store_data(ETHUSDT5MinDataModel, "ETH-USDT-SWAP", "5m", 60 * 5)
    fetch_and_store_data(ETHUSDT3MinDataModel, "ETH-USDT-SWAP", "3m", 60 * 3)
    fetch_and_store_data(ETHUSDT1MinDataModel, "ETH-USDT-SWAP", "1m", 60 * 1)


def update_btc_main():
    fetch_and_store_data(
        BTCUSDTWeekDataModel, "BTC-USDT-SWAP", "1Wutc", 60 * 60 * 24 * 7
    )
    fetch_and_store_data(BTCUSDTDayDataModel, "BTC-USDT-SWAP", "1Dutc", 60 * 60 * 24)
    fetch_and_store_data(BTCUSDT12HDataModel, "BTC-USDT-SWAP", "12Hutc", 60 * 60 * 12)
    fetch_and_store_data(BTCUSDT6HDataModel, "BTC-USDT-SWAP", "6Hutc", 60 * 60 * 6)
    fetch_and_store_data(BTCUSDT4HDataModel, "BTC-USDT-SWAP", "4H", 60 * 60 * 4)
    fetch_and_store_data(BTCUSDT2HDataModel, "BTC-USDT-SWAP", "2H", 60 * 60 * 2)
    fetch_and_store_data(BTCUSDT1HDataModel, "BTC-USDT-SWAP", "1H", 60 * 60 * 1)

def update_btc_detail():
    fetch_and_store_data(BTCUSDT1HDataModel, "BTC-USDT-SWAP", "1H", 60 * 60 * 1)
    fetch_and_store_data(BTCUSDT30MinDataModel, "BTC-USDT-SWAP", "30m", 60 * 30)
    fetch_and_store_data(BTCUSDT15MinDataModel, "BTC-USDT-SWAP", "15m", 60 * 15)
    fetch_and_store_data(BTCUSDT5MinDataModel, "BTC-USDT-SWAP", "5m", 60 * 5)
    fetch_and_store_data(BTCUSDT3MinDataModel, "BTC-USDT-SWAP", "3m", 60 * 3)
    fetch_and_store_data(BTCUSDT1MinDataModel, "BTC-USDT-SWAP", "1m", 60 * 1)


# 获取历史数据并存入数据库
def fetch_and_store_data(model, instId, bar, bar_size, start_timestamp = int(MASK_START_DATE.timestamp() * 1000), end_timestamp = int(datetime.now().timestamp() * 1000)):
    add_timestamp = bar_size * 100 * 1000  # 增加100个单位，单位为毫秒
    aggregate_data = AggregateDataModel.get(AggregateDataModel.table_name == model._meta.table_name)
    if aggregate_data:
        start_timestamp = aggregate_data.record_timestamp if aggregate_data.record_timestamp != 0 else start_timestamp
        while start_timestamp < end_timestamp :
            try:
                print(f"开始请求时间: {datetime.fromtimestamp(start_timestamp / 1000)}")
                # 调用API获取数据
                result = marketDataAPI.get_history_candlesticks(
                    instId=instId, bar=bar, before=start_timestamp-bar_size*1000, after=start_timestamp+bar_size*1000*100, limit=100,
                )
                if result.get("code") == "0":
                    # 按时间倒序的结果
                    data = result.get("data", [])
                    insert_data = []
                    result_max_timestamp = 0
                    result_min_timestamp = end_timestamp
                    for candle in data:
                        timestamp = int(candle[0])
                        insert_data.append({
                            "timestamp":timestamp,  # 时间戳
                            "time":datetime.fromtimestamp(timestamp / 1000),
                            "open":float(candle[1]),  # 开盘价
                            "high":float(candle[2]),  # 最高价
                            "low":float(candle[3]),  # 最低价
                            "close":float(candle[4]),  # 收盘价
                            "volume":float(candle[6]),  # 成交量
                            "turnover":float(candle[7]),  # 成交额
                            "confirm":bool(candle[8]),  # K线状态
                        })
                        result_max_timestamp = max(result_max_timestamp, timestamp)
                        result_min_timestamp = min(result_min_timestamp, timestamp)
                    with model._meta.database.atomic():
                        # 插入数据库
                        model.insert_many(insert_data).on_conflict_replace().execute()
                        with aggregate_db.atomic():
                            aggregate_data.record_timestamp = result_max_timestamp
                            aggregate_data.record_time = datetime.fromtimestamp(result_max_timestamp / 1000)
                            aggregate_data.save()
                    print(
                        f"数据存储完成，时间段：{datetime.fromtimestamp(result_min_timestamp / 1000)} - {datetime.fromtimestamp(result_max_timestamp / 1000)}"
                    )
                    start_timestamp += add_timestamp
                else:
                    print(f"获取数据失败: {result.get('msg')}")
                    time.sleep(0.5)  # 避免触发API速率限制
            except Exception as e:
                print(f"发生错误: {e}")

# 分析趋势
def analyze_trends(model, instId, bar, bar_size, start_timestamp = int(MASK_START_DATE.timestamp() * 1000), end_timestamp = int(datetime.now().timestamp() * 1000)):
    add_timestamp = bar_size * 100 * 1000  # 增加100个单位，单位为毫秒
    aggregate_data = AggregateDataModel.get(AggregateDataModel.table_name == model._meta.table_name)
    if aggregate_data:
        start_timestamp = aggregate_data.trend_timestamp if aggregate_data.trend_timestamp != 0 else start_timestamp
        up_trend, down_trand,  = None
        while start_timestamp < end_timestamp:
            print()

if __name__ == "__main__":
    start_time = time.time()
    # update_all()
    update_eth_month()
    end_time = time.time()
    print(f"Data completed in {end_time - start_time:.2f} seconds.")
