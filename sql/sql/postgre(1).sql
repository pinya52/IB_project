select t1.restaurant_uuid,t1.年份,t1.月份,t1.平台總類,t1.平台金額,t1.平台筆數,t2.新增會員數
from (select restaurant_uuid, EXTRACT(YEAR FROM ioo.created_at) as 年份,
       EXTRACT(MONTH FROM ioo.created_at) as 月份, ioo.platform_type as 平台總類, sum(amount) as 平台金額, count(platform_type) as 平台筆數

        from ichef_online_order as ioo
        left join ichef_online_order_payment as ioop on ioo.id = ioop.online_order_id
        where ioo.restaurant_uuid = 'bfaeaf13-b2fe-4c3e-a6a5-7a040b5c00b4'
        GROUP BY ioo.restaurant_uuid, ioo.platform_type, 年份, 月份
        ) t1
LEFT JOIN (select cm.restaurant_uuid,
         count(distinct(name)) as 新增會員數,
         EXTRACT(YEAR  FROM created_at) as 年份,
         EXTRACT(MONTH FROM created_at) as 月份
        from crm_members cm
        where cm.restaurant_uuid = 'bfaeaf13-b2fe-4c3e-a6a5-7a040b5c00b4'
        and  cm.is_deleted = False
        --      and EXTRACT(YEAR  FROM created_at) = 2020
        --      and EXTRACT(MONTH FROM created_at) = 3
        group by cm.restaurant_uuid, 年份, 月份) t2
ON (t1.restaurant_uuid = t2.restaurant_uuid AND t1.年份 = t2.年份 AND t1.月份 = t2.月份)
order by t1.年份,t1.月份