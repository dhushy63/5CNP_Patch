
import React, { useEffect, useState } from 'react'
import { apiGet } from '../lib/api'

export default function MealPlan({ userId }) {
  const [items, setItems] = useState([])

  useEffect(()=>{
    apiGet(`/meal-plan?user_id=${userId}`).then(d=>setItems(d.meals || []))
  }, [userId])

  return (
    <div style={{ maxWidth: 720 }}>
      <h3>Meal Plan</h3>
      <div style={{ display:'grid', gap: 10 }}>
        {items.map((m,i)=>(
          <div key={i} style={{ border:'1px solid #eee', padding: 12, borderRadius: 12 }}>
            <b style={{ textTransform: 'capitalize' }}>{m.type}</b>: {m.items}
          </div>
        ))}
      </div>
    </div>
  )
}
