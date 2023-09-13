SELECT
       cc.customer_no as 客編,
       cs.name as 店名,
       cc.subscription_activation_date as 系統啟用日,
       cc.subscription_activation_date,
       cc.ichef_next_renewal_date,
       cs.address as 店址,
       ss.awareness as 店家來源,
       ss.contact_channel as 接觸Ichef方式,
       CASE
           WHEN ss.assignment_status = 'introduced' then '電話說明無法指派'
           WHEN ss.assignment_status = 'office_assign' then '指派'
           WHEN ss.assignment_status = 'sales_assign' then '指派'
           WHEN ss.assignment_status = 'sales_referral' then '轉介'
           WHEN ss.assignment_status = 'sales_cold_visit' then '轉介'
           WHEN ss.assignment_status = 'vip' then '轉介'
           WHEN ss.assignment_status = 'third_party_refer' THEN '轉介'

        END AS 通路,
    CASE
           WHEN restaurant_food_type = 'type_01' THEN '早(午)餐店/三明治/蛋餅店'
           WHEN restaurant_food_type = 'type_02' THEN '茶飲/冷熱飲/咖啡廳'
           WHEN restaurant_food_type = 'type_03' THEN '自助快餐/便當店'
           WHEN restaurant_food_type = 'type_04' THEN '健康料理/沙拉/素食料理店'
           WHEN restaurant_food_type = 'type_05' THEN '火鍋店'
           WHEN restaurant_food_type = 'type_06' THEN '台式餐廳'
           WHEN restaurant_food_type = 'type_07' THEN '台式小吃'
           WHEN restaurant_food_type = 'type_08' THEN '燒烤店'
           WHEN restaurant_food_type = 'type_09' THEN '烘焙麵包/蛋糕/糕點甜點店'
           WHEN restaurant_food_type = 'type_10' THEN '甜品/挫冰店'
           WHEN restaurant_food_type = 'type_11' THEN '飲酒店/酒吧/居酒屋/餐酒館'
           WHEN restaurant_food_type = 'type_12' THEN '客家/原住民/中港澳餐廳/鐵板燒'
           WHEN restaurant_food_type = 'type_13' THEN '美式餐廳'
           WHEN restaurant_food_type = 'type_14' THEN '日式餐廳/日式小吃'
           WHEN restaurant_food_type = 'type_15' THEN '韓式餐廳/韓式小吃'
           WHEN restaurant_food_type = 'type_16' THEN '歐式(英/法/義/瑞/其他)餐廳'
           WHEN restaurant_food_type = 'type_17' THEN '東南亞(印/泰/越/馬/新)餐廳'
           WHEN restaurant_food_type = 'type_18' THEN '他國(中東/非洲/俄羅斯)餐廳'
           WHEN restaurant_food_type = 'type_19' THEN '親子餐廳/寵物友善餐廳'
           WHEN restaurant_food_type = 'type_20' THEN '其他非餐飲之零售或服務業'

       END AS 餐廳類型



FROM customers_customer cc
LEFT JOIN customers_store cs on cc.id = cs.customer_id
LEFT JOIN sales_saleslead ss on cc.customer_no = ss.customer_no
LEFT JOIN users_user on users_user.id = ss.assigned_to_id

WHERE subscription_activation_date != ichef_next_renewal_date -- 至少有付錢
And ichef_next_renewal_date >= '2019-01-01' -- 續約時間超過今天 即 排除欠款店家
AND cc.subscription_activation_date < '2023-01-01'
-- AND    ( cc.ichef_subscription_cancellation_date IS NULL   OR   cc.ichef_subscription_cancellation_date >= NOW() ) -- 合約終止時間在目前時間之後 或是 沒有壓合約中止時間
AND cs.name is not null