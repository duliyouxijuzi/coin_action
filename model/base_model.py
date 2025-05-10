from peewee import Model, BigIntegerField, DateTimeField, FloatField, BooleanField, IntegerField


# 定义基础数据模型
class BaseDataModel(Model):
    timestamp = BigIntegerField(primary_key=True, unique=True)
    time = DateTimeField()
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    volume = FloatField()
    turnover = FloatField()
    confirm = BooleanField()

    class Meta:
        abstract = True


# 定义具有趋势的数据模型
class BaseTrendDataModel(BaseDataModel):
    # -3 下降趋势
    # -2 自然回落
    # -1 次级回落
    # 0 无变化
    # +1 次级回升
    # +2 自然回升
    # +3 上升趋势
    trend = IntegerField(default=0)
    redmask = BooleanField(default=False)
    greenmask = BooleanField(default=False)

    class Meta:
        abstract = True

