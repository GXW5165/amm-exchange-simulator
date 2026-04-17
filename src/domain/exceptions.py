class AMMError(Exception):
    pass


class PoolNotInitializedError(AMMError):
    pass


class InsufficientBalanceError(AMMError):
    pass


class InsufficientLiquidityError(AMMError):
    pass


class InvalidEventError(AMMError):
    pass
