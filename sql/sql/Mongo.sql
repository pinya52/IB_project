
(select
restaurant_uuid,
storeID,
EXTRACT(YEAR FROM operated_at) as 年份,
EXTRACT(MONTH FROM operated_at) as 月份,
count(total_amount) total_count,
sum(total_amount) price_total_amount,
count(*) filter( where discount_amount>0) discount_count ,
sum(discount_amount) discount_amount,
sum(people) people,
count(distinct meal_category) meal_category_count,
round(sum(total_amount)::numeric /sum(people)::numeric ,2) as 平均客單價,
count(*) filter( where payment_type='cash') cash ,
count(*) filter( where payment_type='credit_card') credit_card ,
count(*) filter( where payment_type='other_payment') other_payment ,
sum(case when payment_type='cash' then total_amount else 0 END) cash_total,
sum(case when payment_type='credit_card' then total_amount else 0 END) credit_total,
sum(case when payment_type='other_payment' then total_amount else 0 END) other_payment_total,
count(*) filter( where service_type='indoor') indoor,
count(*) filter( where service_type='takeout') takeout,
sum(case when service_type='indoor' then total_amount else 0 END) indoor_total,
sum(case when service_type='takeout' then total_amount else 0 END) takeout_total,
sum(case when total_amount < 200  then total_amount else 0 END) under_200,
sum(case when total_amount >= 200 and total_amount < 600 then total_amount else 0 END) under_600,
sum(case when total_amount >= 600  then total_amount else 0 END) over_600,
count(*) filter( where total_amount < 200) under_200_ppl,
count(*) filter( where total_amount >= 200 and total_amount < 600) under_600_ppl,
count(*) filter( where total_amount >= 600) over_600_ppl,
sum( case when to_char(operated_at, 'HH24')>='05' and to_char(operated_at, 'HH24') < '11' then total_amount else 0 END) total_from_5_11,
count(*) filter( where to_char(operated_at, 'HH24')>='05' and to_char(operated_at, 'HH24') < '11') ppl_from_5_11,
sum( case when to_char(operated_at, 'HH24')>='11' and to_char(operated_at, 'HH24') < '15' then total_amount else 0 END) total_from_11_15,
count(*) filter( where to_char(operated_at, 'HH24')>='11' and to_char(operated_at, 'HH24') < '15') ppl_from_11_15,
sum( case when to_char(operated_at, 'HH24')>='15' and to_char(operated_at, 'HH24') < '18' then total_amount else 0 END) total_from_15_18,
count(*) filter( where to_char(operated_at, 'HH24')>='15' and to_char(operated_at, 'HH24') < '18') ppl_from_15_18,
sum( case when to_char(operated_at, 'HH24')>='18' and to_char(operated_at, 'HH24') < '22' then total_amount else 0 END) total_from_18_22,
count(*) filter( where to_char(operated_at, 'HH24')>='18' and to_char(operated_at, 'HH24') < '22') ppl_from_18_22,
sum( case when to_char(operated_at, 'HH24')>='22' and to_char(operated_at, 'HH24') < '24' then total_amount else 0 END)+sum( case when to_char(operated_at, 'HH24')>='01' and to_char(operated_at, 'HH24') < '05' then total_amount else 0 END) total_from_22_5,
count(*) filter( where to_char(operated_at, 'HH24')>='22' and to_char(operated_at, 'HH24') < '24')+count(*) filter( where to_char(operated_at, 'HH24')>='01' and to_char(operated_at, 'HH24') < '05') ppl_from_22_5,
AVG(EXTRACT(MINUTE FROM time_diff)) as time_diff



from
(select
(op._doc #>> '{ invoice,total_amount }')::float total_amount,
(op._doc #>> '{ restaurant_uuid }')::text restaurant_uuid,
(op._doc #>> '{ iCHEF_storeID }')::text storeID,
(op._doc #>> '{ invoice,discount_amount }')::float discount_amount,
(op._doc #>> '{ invoice,customer_group,people }')::float people,
(op._doc #>> '{ invoice,customer_group,service_type }')::text service_type,
(op._doc #>> '{ invoice,service_charge }')::text service_charge,
(CASE
        WHEN (op._doc #>> '{ invoice,invoice_payment,0,payment_type }') = 'cash'  THEN 'cash'
        WHEN (op._doc #>> '{ invoice,invoice_payment,0,payment_type }') = 'credit_card' THEN 'credit_card'
        ELSE  'other_payment'
END) as payment_type,

(op._doc #>> '{ invoice,customer_order,0,item_order,category,name }')::text meal_category,

inv.restaurant_id,
inv.created_at-inv.operated_at   AS time_diff,
inv.operated_at,
inv.created_at

from mongo2psql_invoice inv join mongo2psql_invoiceoperation op on op.id = inv.create_operation_id

where
inv.is_cancelled = 'f'
and inv.restaurant_id = 9037
and inv.operated_at between '2019-1-01 00:00:00.000001' and  '2022-12-31 23:59:59.999999'

--16:00 = 00:00  21:00 = 5:00
--15:59 = 23:59
) tmp

group by restaurant_uuid, storeID,年份,月份
order by storeID
)