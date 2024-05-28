import pandas as pd
import itertools
import math
import os.path

def cal_book_d(param, gr_bid_level, gr_ask_level, diff, var):

    ratio = param[0]
    level = param[1]
    interval = param[2]

    decay = math.exp(-1.0/interval)
    
    _flag = var['_flag']                            #맨 처음인 경우 True
    curBidQty = gr_bid_level['quantity'].sum()
    curAskQty = gr_ask_level['quantity'].sum()
    curBidTop = gr_bid_level.iloc[0].price #what is current bid top?
    curAskTop = gr_ask_level.iloc[0].price
    if _flag:
        var['prevBidQty'] = curBidQty
        var['prevAskQty'] = curAskQty
        var['prevBidTop'] = curBidTop
        var['prevAskTop'] = curAskTop
        var['bidSideAdd'] = 0
        var['bidSideDelete'] = 0
        var['askSideAdd'] = 0
        var['askSideDelete'] = 0
        var['bidSideTrade'] = 0
        var['askSideTrade'] = 0
        var['bidSideFlip'] = 0
        var['askSideFlip'] = 0
        var['bidSideCount'] = 0
        var['askSideCount'] = 0
        var['_flag'] = False
        return 0.0


    prevBidQty = var['prevBidQty']
    prevAskQty = var['prevAskQty']
    prevBidTop = var['prevBidTop']
    prevAskTop = var['prevAskTop']
    bidSideAdd = var['bidSideAdd']
    bidSideDelete = var['bidSideDelete']
    askSideAdd = var['askSideAdd']
    askSideDelete = var['askSideDelete']
    bidSideTrade = var['bidSideTrade']
    askSideTrade = var['askSideTrade']
    bidSideFlip = var['bidSideFlip']
    askSideFlip = var['askSideFlip']
    bidSideCount = var['bidSideCount']
    askSideCount = var['askSideCount'] 
        
    if curBidQty > prevBidQty:
        bidSideAdd += 1
        bidSideCount += 1
    if curBidQty < prevBidQty:
        bidSideDelete += 1
        bidSideCount += 1
    if curAskQty > prevAskQty:
        askSideAdd += 1
        askSideCount += 1
    if curAskQty < prevAskQty:
        askSideDelete += 1
        askSideCount += 1
        
    if curBidTop < prevBidTop:
        bidSideFlip += 1
        bidSideCount += 1
    if curAskTop > prevAskTop:
        askSideFlip += 1
        askSideCount += 1

    
    (_count_1, _count_0, _units_traded_1, _units_traded_0, _price_1, _price_0) = get_diff_count_units(diff)
    
    bidSideTrade += _count_1
    bidSideCount += _count_1
    
    askSideTrade += _count_0
    askSideCount += _count_0
    

    if bidSideCount == 0:
        bidSideCount = 1
    if askSideCount == 0:
        askSideCount = 1

    bidBookV = (-bidSideDelete + bidSideAdd - bidSideFlip) / (bidSideCount**ratio)
    askBookV = (askSideDelete - askSideAdd + askSideFlip ) / (askSideCount**ratio)
    tradeV = (askSideTrade/askSideCount**ratio) - (bidSideTrade / bidSideCount**ratio)
    bookDIndicator = askBookV + bidBookV + tradeV
        
       
    var['bidSideCount'] = bidSideCount * decay #exponential decay
    var['askSideCount'] = askSideCount * decay
    var['bidSideAdd'] = bidSideAdd * decay
    var['bidSideDelete'] = bidSideDelete * decay
    var['askSideAdd'] = askSideAdd * decay
    var['askSideDelete'] = askSideDelete * decay
    var['bidSideTrade'] = bidSideTrade * decay
    var['askSideTrade'] = askSideTrade * decay
    var['bidSideFlip'] = bidSideFlip * decay
    var['askSideFlip'] = askSideFlip * decay

    var['prevBidQty'] = curBidQty
    var['prevAskQty'] = curAskQty
    var['prevBidTop'] = curBidTop
    var['prevAskTop'] = curAskTop
 
    return bookDIndicator


def get_diff_count_units (diff):
    
    _count_1 = _count_0 = _units_traded_1 = _units_traded_0 = 0
    _price_1 = _price_0 = 0

    diff_len = len (diff)
    if diff_len == 1:
        row = diff.iloc[0]
        if row['type'] == 1:
            _count_1 = row['count']
            _units_traded_1 = row['units_traded']
            _price_1 = row['price']
        else:
            _count_0 = row['count']
            _units_traded_0 = row['units_traded']
            _price_0 = row['price']

        return (_count_1, _count_0, _units_traded_1, _units_traded_0, _price_1, _price_0)

    elif diff_len == 2:
        row_1 = diff.iloc[1]
        row_0 = diff.iloc[0]
        _count_1 = row_1['count']
        _count_0 = row_0['count']

        _units_traded_1 = row_1['units_traded']
        _units_traded_0 = row_0['units_traded']
        
        _price_1 = row_1['price']
        _price_0 = row_0['price']

        return (_count_1, _count_0, _units_traded_1, _units_traded_0, _price_1, _price_0)
    

def cal_book_i(param, gr_bid_level, gr_ask_level, mid):
    
    mid_price = mid

    ratio = param[0]
    level = param[1]
    interval = param[2]

    quant_v_bid = gr_bid_level.quantity**ratio
    price_v_bid = gr_bid_level.price * quant_v_bid

    quant_v_ask = gr_ask_level.quantity**ratio
    price_v_ask = gr_ask_level.price * quant_v_ask
 
        
    askQty = quant_v_ask.values.sum()
    bidPx = price_v_bid.values.sum()
    bidQty = quant_v_bid.values.sum()
    askPx = price_v_ask.values.sum()
    bid_ask_spread = interval
        
    book_price = 0 #because of warning, divisible by 0
    if bidQty > 0 and askQty > 0:
        book_price = (((askQty*bidPx)/bidQty) + ((bidQty*askPx)/askQty)) / (bidQty+askQty)

        
    indicator_value = (book_price - mid_price) / bid_ask_spread
    return indicator_value


def truncate(f, n):
    #'''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def cal_mid_price (gr_bid_level, gr_ask_level):

    level = 5
    
    if len(gr_bid_level) > 0 and len(gr_ask_level) > 0:
        bid_top_price = gr_bid_level.iloc[0].price
        bid_top_level_qty = gr_bid_level.iloc[0].quantity
        ask_top_price = gr_ask_level.iloc[0].price
        ask_top_level_qty = gr_ask_level.iloc[0].quantity
    
        mid_price_top = (bid_top_price + ask_top_price) * 0.5 #what is mid price?
        mid_price_wt = ((gr_bid_level.head(level))['price'].mean() + (gr_ask_level.head(level))['price'].mean()) * 0.5
        
        #runtimeWarning 방지
        if(bid_top_level_qty+ask_top_level_qty == 0):
            mid_price_mkt = 0
        else: 
            mid_price_mkt = ((bid_top_price*ask_top_level_qty) + (ask_top_price*bid_top_level_qty))/(bid_top_level_qty+ask_top_level_qty)
        mid_price_mkt = truncate(mid_price_mkt, 1)
        
        return (mid_price_top, mid_price_wt, mid_price_mkt)

    else:
        print ('Error: serious cal_mid_price')
        return (-1)
    

def cal_mid_price_vwap(total_list, trunit_list):
    totalsum = 0
    unitsum = 0
    #가중평균: 10개의 sample 취함
    if(len(total_list)<10):
        return 0
    for i in range (-10, 0):
        totalsum += total_list[i]
        unitsum += trunit_list[i]

    if(unitsum ==0 ):
        return -1
    mid_price_vwap = totalsum/unitsum
    mid_price_vwap = truncate(mid_price_vwap, 1)
    return mid_price_vwap
    

def cal_rsi(diff):
    au = 0
    ad = 0
    u_count=0
    d_count=0
    if(len(diff) < 10):
        return 0
    else:
        for i in range (-10, 0):
            if(diff[i]<0):
                ad-=diff[i]
                d_count += 1
            elif(diff[i]>0):
                au+=diff[i]
                u_count += 1
        if(d_count == 0):
            return 100
        if(u_count == 0):
            return 0
        ad = ad/d_count
        au = au/u_count
        rs = au/ad
        rsi = 100* rs/(1+rs)
        return rsi

def main():
    #아래 두 개는 주어진 5/1일 file 읽을 것임: for
    df_o = pd.read_csv('2024-05-01-upbit-BTC-book.csv').apply(pd.to_numeric, errors='ignore')
    group_o = df_o.groupby('timestamp')

    df_t = pd.read_csv('2024-05-01-upbit-BTC-trade.csv').apply(pd.to_numeric, errors='ignore')
    group_t = df_t.groupby('timestamp')

    var = {}
    var['_flag'] = True

    prev_price = 0.0
    diff = []
    total_list = []
    trunit_list = []
    for(gr_o_tu, gr_t_tu) in itertools.zip_longest(group_o, group_t):                 #두 group 모두 1초 단위로 잘림
        gr_o = gr_o_tu[1]
        gr_t = gr_t_tu[1]

        gr_o_bid_level = gr_o[(gr_o['type'] == 0)]
        gr_o_ask_level = gr_o[(gr_o['type'] == 1)]
        cur_price = (gr_t.iloc[0])['price']
        diff.append(cur_price - prev_price)
        total_list.append((gr_t.iloc[0])['total'])
        trunit_list.append((gr_t.iloc[0])['units_traded'])
        prev_price = cur_price
        mid_top, mid_wt, mid_mkt = cal_mid_price(gr_o_bid_level, gr_o_ask_level)
        mid_vwap = cal_mid_price_vwap(total_list, trunit_list)
        rsi = cal_rsi(diff)


    
        #(ratio, level, interval seconds): Book imbalance와 book delta는 ratio, level, interval, mid price의 선택에 따라 여러 조합 만들어낼 수 있음. 이 경우에는 임의로 정한 한 가지 조합만 수행.
        book_imbalance_params = (0.2, 15, 1) 
        book_delta_params = (0.2,15,1)

        bookI = cal_book_i(book_imbalance_params, gr_o_bid_level, gr_o_ask_level, mid_top)  #First line skip의 이유가 없는 듯 해 var 사용 안함
        bookD = cal_book_d(book_delta_params, gr_o_bid_level, gr_o_ask_level, gr_t, var)

        res_df_given = pd.DataFrame({
            "mid_price_top": [mid_top],
            "mid_price_weighted": [mid_wt],
            "mid_price_market": [mid_mkt],
            "mid_price_vwap": [mid_vwap],
            "book-imbalance-%d-%d-%d" %(book_imbalance_params[0], book_imbalance_params[1], book_imbalance_params[2]) : [bookI],
            "book-delta-%d-%d-%d" %(book_delta_params[0], book_delta_params[1], book_delta_params[2]) : [bookD],
            "rsi" : [rsi],
            "timestamp": [gr_o_tu[0]]
        })

        if(not os.path.isfile("%s-upbit-feature.csv"%('2024-05-01'))):
            res_df_given.to_csv("%s-upbit-feature.csv"%('2024-05-01'), index=False, mode = 'a', sep='|')
        else:
            res_df_given.to_csv("%s-upbit-feature.csv"%('2024-05-01'), index=False, header=False, mode = 'a', sep='|')

    

    #project 1서 만든 file 이용: trade data 없으므로 trade data 이용하는 indicator 제외
    #project 1서 만든 bitthumb file 모두 읽기
    #2024-04-22 to 2024-04-23
    
    for i in range (2):
        df = pd.read_csv('book-2024-04-%d-bithumb.csv' %(i+22),sep='|').apply(pd.to_numeric, errors='ignore')
        group_o_my = df.groupby('timestamp')

        for gr_o_my_tu in group_o_my:
            gr_o_my = gr_o_my_tu[1]
            gr_o_bid_level = gr_o_my[(gr_o_my['type'] == 0)]
            gr_o_ask_level = gr_o_my[(gr_o_my['type'] == 1)]
            mid_top, mid_wt, mid_mkt = cal_mid_price(gr_o_bid_level, gr_o_ask_level)

            book_imbalance_params = (0.2, 15, 1)
            bookI = cal_book_i(book_imbalance_params, gr_o_bid_level, gr_o_ask_level, mid_top)

            res_df_given = pd.DataFrame({
                "mid_price_top": mid_top,
                "mid_price_weighted": mid_wt,
                "mid_price_market": mid_mkt,
                "book-imbalance-%d-%d-%d" %(book_imbalance_params[0], book_imbalance_params[1], book_imbalance_params[2]) : bookI,
                "timestamp": gr_o_my_tu[0]
            },index=[0])
            output_file_path = "04-22to23-bithumb-feature.csv"
            if not os.path.isfile(output_file_path):
                res_df_given.to_csv(output_file_path, index=False, mode='a', sep='|')
            else:
                res_df_given.to_csv(output_file_path, index=False, header=False, mode='a', sep='|')


if __name__ == "__main__":
    main()

