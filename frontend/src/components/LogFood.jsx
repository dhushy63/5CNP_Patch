
import React, { useEffect, useState } from 'react'
import { apiGet, apiPost } from '../lib/api'

export default function LogFood({ userId }) {
  const [text, setText] = useState('2 chapatis with dal and yogurt')
  const [items, setItems] = useState([])

  const load = ()=> apiGet(`/food/recent?user_id=${userId}`).then(d=>setItems(d.items || []))

  useEffect(()=>{ load() }, [userId])

  const add = async () => {
    await apiPost('/food', { user_id: userId, description: text })
    setText('')
    await load()
  }

  return (
    <div style={{ maxWidth: 700 }}>
      <div style={{ display: 'flex', gap: 8 }}>
        <input value={text} onChange={e=>setText(e.target.value)} style={{ flex: 1, padding: 10, borderRadius: 12, border: '1px solid #ddd' }}/>
        <button onClick={add} style={{ padding: '8px 16px', borderRadius: 12, border: '1px solid #ddd' }}>Log</button>
      </div>
      <ul style={{ marginTop: 16 }}>
        {items.map((it, i)=>(<li key={i} style={{ padding: 8, borderBottom: '1px solid #eee' }}><b>{new Date(it.ts).toLocaleString()}</b>: {it.description}</li>))}
      </ul>
    </div>
  )
}
