
  select restaurant_uuid,
         EXTRACT(YEAR FROM created_at)  as 年份,
         EXTRACT(MONTH FROM created_at) as 月份,
         sum(delta) as 集點數,
         count(type) as 兌換比數,
         type
    from crm_club_point as cp
    where restaurant_uuid = '88ee4f97-2869-4c79-842b-b01664f85052'
    and type = 'redeem'
group by restaurant_uuid, 年份, 月份, type
order by 年份, 月份