import orderbook


def test_firstLimitOrder():
    assert orderbook.newLimitOrder(
        "BUY",
        1,
        100,
        "BTCZAR",
        False) == "Order placed."

    assert len(orderbook.btcBids) == 1
    assert orderbook.btcBids[0] == {"quantity": 1, "price": 100}


def test_additionalLimitOrdersPlacedCorrectly():
    assert orderbook.newLimitOrder(
        "BUY",
        1,
        150,
        "BTCZAR",
        False) == "Order placed."

    assert orderbook.newLimitOrder(
        "BUY",
        1,
        50,
        "BTCZAR",
        False) == "Order placed."

    assert len(orderbook.btcBids) == 3
    assert orderbook.btcBids[0] == {"quantity": 1, "price": 150}
    assert orderbook.btcBids[1] == {"quantity": 1, "price": 100}
    assert orderbook.btcBids[2] == {"quantity": 1, "price": 50}


def test_nonMatchingLimitOrder():
    assert orderbook.newLimitOrder(
        "SELL",
        1,
        200,
        "BTCZAR",
        False) == "Order placed."

    assert len(orderbook.btcAsks) == 1
    assert len(orderbook.btcBids) == 3
    assert orderbook.btcAsks[0] == {"quantity": 1, "price": 200}
    assert orderbook.btcBids[0] == {"quantity": 1, "price": 150}
    assert orderbook.btcBids[1] == {"quantity": 1, "price": 100}
    assert orderbook.btcBids[2] == {"quantity": 1, "price": 50}


def test_matchingLimitOrderFilled():
    assert orderbook.newLimitOrder(
        "SELL",
        0.5,
        100,
        "BTCZAR",
        False) == "Order completely filled."

    assert len(orderbook.btcAsks) == 1
    assert len(orderbook.btcBids) == 3
    assert orderbook.btcAsks[0] == {"quantity": 1, "price": 200}
    assert orderbook.btcBids[0] == {"quantity": 0.5, "price": 150}
    assert orderbook.btcBids[1] == {"quantity": 1, "price": 100}
    assert orderbook.btcBids[2] == {"quantity": 1, "price": 50}


def test_matchingLimitOrderNotFilled():
    assert orderbook.newLimitOrder(
        "SELL",
        2,
        100,
        "BTCZAR",
        False) == "Order partially filled. Remainder placed in orderbook."

    assert len(orderbook.btcAsks) == 2
    assert len(orderbook.btcBids) == 1
    assert orderbook.btcAsks[0] == {"quantity": 0.5, "price": 100}
    assert orderbook.btcAsks[1] == {"quantity": 1, "price": 200}
    assert orderbook.btcBids[0] == {"quantity": 1, "price": 50}


def test_postOnlyLimitOrder():
    assert orderbook.newLimitOrder(
        "SELL",
        1,
        75,
        "BTCZAR",
        True) == "Order placed."

    assert orderbook.newLimitOrder(
        "SELL",
        1,
        50,
        "BTCZAR",
        True) == "Post Only order cancelled as it would have matched."

    assert len(orderbook.btcAsks) == 3
    assert len(orderbook.btcBids) == 1
    assert orderbook.btcAsks[0] == {"quantity": 1, "price": 75}
    assert orderbook.btcAsks[1] == {"quantity": 0.5, "price": 100}
    assert orderbook.btcAsks[2] == {"quantity": 1, "price": 200}
    assert orderbook.btcBids[0] == {"quantity": 1, "price": 50}


def test_getOrderbook():
    assert orderbook.getOrderbook("BTCZAR") == {
        "Asks": [
            {"quantity": 1, "price": 75},
            {"quantity": 0.5, "price": 100},
            {"quantity": 1, "price": 200}
        ],
        "Bids": [
            {"quantity": 1, "price": 50}
        ]
    }


def test_getTradeHistory():
    assert orderbook.getTradeHistory(
        "BTCZAR",
        100) == {
            "TradeHistory": [
                {"quantity": 1, "price": 100, "takerSide": "sell"},
                {"quantity": 0.5, "price": 150, "takerSide": "sell"},
                {"quantity": 0.5, "price": 150, "takerSide": "sell"}
            ]
        }

    assert orderbook.getTradeHistory("BTCZAR", 1) == {"TradeHistory": [
        {"quantity": 1, "price": 100, "takerSide": "sell"}]}
