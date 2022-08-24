DECLARE @tem table(
		stock_code varchar(10),
		ma real
	)
DECLARE @company VARCHAR(10)

DECLARE cur CURSOR LOCAL for
		SELECT stock_code FROM stock_list where isTaiwan50 = 1
open cur
FETCH next from cur into @company

WHILE @@FETCH_STATUS = 0 
	BEGIN
		insert into @tem(stock_code, ma)
		select @company, AVG(c) from stock_data
		where stock_code = @company and 
		date between '2022-05-17' and '2022-05-23'

		FETCH next from cur into @company
	END
close cur

select * from @tem

