Drop table if exists #temp2
select * into #temp2 from
	(select distinct Party_code from
		(SELECT CONCAT(left(CONVERT(VARCHAR(20),ts),4),'-',SUBSTRING(CONVERT(VARCHAR(20),ts),5,2),'-',SUBSTRING(CONVERT(VARCHAR(20),ts), 7, 2))
		as Newdate, 
		profile_identity as Party_code 
		from [OnlineEngine].[dbo].[CT_NotificationClicked]
		where 
		SUBSTRING(campaignid, 1, len(campaignid)-9) IN ('145161') 
		and CONCAT(left(CONVERT(VARCHAR(20),ts),4), '-',SUBSTRING(CONVERT(VARCHAR(20),ts),5,2),'-',SUBSTRING(CONVERT(VARCHAR(20),ts), 7, 2)) >='2022-11-18' 
		and CONCAT(left(CONVERT(VARCHAR(20),ts),4), '-',SUBSTRING(CONVERT(VARCHAR(20),ts),5,2),'-',SUBSTRING(CONVERT(VARCHAR(20),ts), 7, 2)) <='2022-11-18'
		)as A
	)as B
select B.* from #temp2 as A
left join [Communication].[dbo].[UB_FNO] as B
on A.party_code = B.party_code
where FNOSauda_Date is not null
order by FNOSauda_Date