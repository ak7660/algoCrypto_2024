# EMAs and MACD Hybrid high-frequency algorithmic strategy for BTCUSD

This project was developed as part of my participation in the AlgoGene platform's trading competition, specifically within the cryptocurrency stream as a member of Team G.

## Project Overview

Our team, Team G, initially aimed to collaborate closely on this project. However, due to simultaneous travel commitments among all three members, coordination proved challenging. As a result, I took on the majority of the development work independently.

## Development Phases

- **First Round:** Under tight deadlines and amidst our travels, I managed to code the initial algorithm in roughly two hours on the final day of submission. Despite these constraints, our entry was successful enough to advance us to the next stage.

- **Second Round:** This phase involved live testing of our algorithm in the real market. Although the testing period spanned from January to February, we only deployed our algorithm at the beginning of February. After returning to university in the last week of January, I dedicated time to develop and rigorously test a new algorithm. This revised version demonstrated significantly high returns, validating the effectiveness of our strategies under live market conditions.

Despite the limited time of deployment in the live market, our algorithm quickly rose to the top of the live return table. When later the results were released, we still maintained the highest live return among the competitors. However, we were not shortlisted for the finals. The selection criteria considered both rounds of submissions, and despite my request, the first round submission could not be updated. Our effective strategy, which was deployed later in February, was not reflected in the initial evaluation.

This repository includes all the code related to the project. You will also find screenshots from the AlgoGene platform, showcasing the results of both backtests and live tests. For the live test, the algorithm was allowed to run until the end of March, achieving an impressive live return of approximately 800%.

## Trading Strategy
This script implements a cryptocurrency trading strategy using BTCUSD (Bitcoin), utilizing multiple technical analysis indicators to drive trading decisions. Here's a brief overview of the trading logic:

### Parameters Used
Initial Capital: 100000 USD
Levergae: 10x
Benchmark: BTCUSD

### Day Trade:
Buy Signal: When the short-period EMA is above the medium, which is above the long, which in turn is above the extra-long period EMA.
Sell Signal: When the short-period EMA is below the medium, which is below the long, which in turn is below the extra-long period EMA. This strategy aims to capture trends by entering positions at the start of potential new trends indicated by EMA crossovers.

### Hourly Trades
Buy Signal: When the MACD line crosses above the signal line and the price is between the middle and upper Bollinger Band.
Sell Signal: When the MACD line crosses below the signal line and the price is between the middle and lower Bollinger Band. Trades are executed based on these signals, and positions are adjusted dynamically with market conditions.

(I didn't used any stoploss as whenever a new crossover will happen, all the previous trades are closed which acts a stoploss too. Other indicators that I tried and can be implemneted to optimize are ATR and bollinger bands)

Feel free to explore the repository and reach out if you have any questions or suggestions!



![](poptart1redrainbowfix_1.gif)

