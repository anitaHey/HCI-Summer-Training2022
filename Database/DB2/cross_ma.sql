select stock_data.stock_code, AVG(c) from stock_data
cross apply(
	select stock_code from stock_list where isTaiwan50 =1
) T1
where T1.stock_code = stock_data.stock_code and 
	stock_data.date between '2022-05-17' and '2022-05-23'
group by stock_data.stock_code


