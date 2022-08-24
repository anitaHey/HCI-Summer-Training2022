DECLARE @remaining_day int;
DECLARE @current_day int;
DECLARE @NumberOfDay int;
DECLARE @Date date;

SET @NumberOfDay = 10
SET @Date = '2022-01-04'

SELECT @current_day = day_of_stock FROM [dbo].[calendar] WHERE date = @Date AND day_of_stock != -1;
if(@current_day is NULL) RETURN
SET @remaining_day = @current_day - @NumberOfDay;

IF(@remaining_day > 0)
	SELECT * FROM [dbo].[calendar] WHERE day_of_stock BETWEEN @remaining_day AND @current_day AND year(date) = year(@Date);
ELSE 
	BEGIN
		SELECT * FROM [dbo].[calendar] WHERE day_of_stock BETWEEN 0 AND @current_day AND year(date) = year(@Date);

		DECLARE cur CURSOR LOCAL for
		SELECT year, total_day FROM [dbo].[year_calendar] order by year DESC
		open cur

		DECLARE @current_year INT
		DECLARE @current_total_day INT
		FETCH next from cur into @current_year, @current_total_day
		WHILE @@FETCH_STATUS = 0 BEGIN
			SET @remaining_day = @remaining_day + @current_total_day;

			IF @remaining_day > 0 
				BEGIN
					SELECT * FROM [dbo].[calendar] WHERE day_of_stock BETWEEN @remaining_day AND @current_total_day AND year(date) = @current_year;
					BREAK
				END
			ELSE
				SELECT * FROM [dbo].[calendar] WHERE day_of_stock BETWEEN 0 AND @current_total_day AND year(date) = @current_year;
			FETCH next from cur into @current_year, @current_total_day
		END
	END