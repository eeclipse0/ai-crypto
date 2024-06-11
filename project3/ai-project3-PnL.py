import pandas as pd

# 데이터 파일을 pandas DataFrame으로 읽어오기
df = pd.read_csv('ai-crypto-project-3-live-btc-krw.csv').apply(pd.to_numeric, errors='ignore')

#bid, ask 구분해서 df 생성
bid_orders = (df[df['side'] == 0])
ask_orders = (df[df['side'] == 1])

trades = []

for idx_bid, bid_order in bid_orders.iterrows():
    matching_ask_orders = ask_orders[ask_orders['quantity'] == bid_order['quantity']] #ask_orders에서 bid_orders와 quantity가 같은 값들 추출
    for idx_ask, ask_order in matching_ask_orders.iterrows():
        trade1 = {
            'timestamp': bid_order['timestamp'],
            'amount': bid_order['amount'],
            'side': bid_order['side']
        }
        trade2 = {
            'timestamp': ask_order['timestamp'],
            'amount': ask_order['amount'],
            'side': ask_order['side']
        }
        trades.append((trade1, trade2)) # 매치된 짝을 list에 저장
        bid_orders = bid_orders.drop(idx_bid)   # 매치된 매수 주문 삭제
        ask_orders = ask_orders.drop(idx_ask)   # 매치된 매도 주문 삭제
        break  # 하나의 매수 주문에 대해 한 번만 매치
#print(trades)

# bid_orders, ask_orders에서 매치되지 않은 값들의 amount 합
remain_amount = ask_orders['amount'].sum() + bid_orders['amount'].sum()

# 거래별 이익 합을 누적하여 총 이익을 계산
total_PnL = sum(trade[0]['amount'] + trade[1]['amount'] for trade in trades)

print("Total PnL:", total_PnL)
print("remaining amount:", remain_amount)