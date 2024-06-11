# AI & cryotocurrency 
This is an AI & Blockchain class project repository for team 20 students.

## Project 1 explanation
Code bithumb_BTC_assign.py generates bitcoin orderbook data CSV file with data from bithumb exchange. Output file name is "book-year-month-day-bithumb.csv". It builds orderbook of level 5, timestamp = 5 seconds.
Code bithumb_ETH_assign.py generates etherium orderbook data. Output file name is "book-year-month-day-bithumb-eth.csv". Other details are same with bitcoin file.
Note that bitcoin output file name is just "book-year-month-day-bithumb.csv", not "book-year-month-day-bithumb-btc.csv". Maybe "book-year-month-day-bithumb-btc.csv" would be a better name to distinguish bitcoin and etherium orderbook, but we've already got our orderbook files with name "book-year-month-day-bithumb.csv" and changing the code and modify .csv file names to fit into changed code would be some kind of cheat. Sorry for the inconvience if you confused from file names.

## Project 2 explanation
We used both our project 1 data and given orderbook and trade data("2024-05-01-upbit-BTC-book/trade.csv").
And our program generates two result files => "04-22to23-bithumb-feature.csv", "2024-05-01-upbit-feature.csv".
The first file is feature file using project 1 orderbook data. Because we don't have any trade data in project1, this file does not include features using trade data. "2024-05-01-upbit-feature.csv" has features that calculated by using given trade data and orderbook data, so there are more features.
Deleted some large files because they exceed 100MB and I don't want to use git lfs. Refer class repository to get "2024-05-01-upbit-BTC-*.csv"s.

## Project 3 explanation
From given files, we generated lasso model and PnL calculation.
