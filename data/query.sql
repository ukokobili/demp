-- 1.Top Exchanges by Trading Volume
SELECT name, volumeUsd
FROM exchanges
ORDER BY volumeUsd DESC
LIMIT 5;

--2.Trading Pairs Distribution
SELECT name, tradingPairs
FROM exchanges
ORDER BY tradingPairs DESC;

--3.Volume Contribution by Rank
SELECT 
    CASE 
        WHEN rank <= 5 THEN 'Top 5' 
        WHEN rank BETWEEN 6 AND 10 THEN '6-10' 
        ELSE 'Below 10' 
    END AS rank_group,
    SUM(volumeUsd) AS total_volume
FROM exchanges
GROUP BY rank_group;

--4. Socket Support Analysis
SELECT socket, COUNT(*) AS exchange_count
FROM exchanges
GROUP BY socket;

--6.Volume vs. Trading Pairs Correlation
SELECT tradingPairs, volumeUsd
FROM exchanges;