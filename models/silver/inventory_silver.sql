select inv_item_sk, inv_warehouse_sk, count(*) cnt   
from {{ref('bronze_inventory')}} group by inv_item_sk, inv_warehouse_sk